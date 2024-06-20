from flask import Flask, request, render_template, make_response, jsonify
from flask_cors import CORS, cross_origin
from getCustomerDataset import  getCsvDataset
import time
import os
import tempfile
import pandas as pd
import json

from Langchain_Agent import Agent_Executor, SummaryFunc, RetrievalQA, llm, reload


# Global Variables: 儲存資料來渲染表格
Ai_response = ""

# Flask App
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

# Backend API

# 測試用
@app.route('/get_test', methods=['POST', 'OPTIONS'])
@cross_origin()
def test_input():
    
    header={
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST'
    }

    sqlCommand = '''
        SELECT *
        FROM 客戶交易資料表
    '''
    data = request.get_json()
    SummaryFunc.Input_Question = data.get('inputText')
    result = SummaryFunc.store_dataset(getCsvDataset.dataset_query_sql("./database/Oracle", sqlCommand))

    return make_response(jsonify({'response': "測試", 'data': result.to_json(orient='records')}), 200, header)

@app.route('/get_summary_test', methods=['POST', 'OPTIONS'])
@cross_origin()
def get_summary_test():
    
    header={
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST'
    }

    try:
        data = request.get_json()
        user_input = data.get('inputText')
        SummaryFunc.Input_Question = user_input
        with open(SummaryFunc.test_folder + SummaryFunc.test_jsonfile, 'r') as f:
            data = json.load(f)
            if user_input in data.keys():
                temp = pd.read_csv(SummaryFunc.test_folder + data[user_input], encoding='utf-8')
                SummaryFunc.store_dataset(temp, True)

                start = time.time()
                result = SummaryFunc.summary()
                end = time.time()

                print(f"\nTotal Summary time: {end - start}")
            else:
                result = "沒有這個查詢結果"

    except Exception as e:
        result = "我不知道怎麼回答"
        print(f'\nThe error message is here: {e}')

    return make_response(jsonify({'response': result}), 200, header)

# SQL
@app.route('/get_answer', methods=['POST', 'OPTIONS'])
@cross_origin()
def process_input():

    global Ai_response

    header={
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST'
    }

    data = request.get_json()
    print(f'server receive data from User input: {data}')
    user_input = data.get('inputText') #等同於 data['inputText']
    try:
        SummaryFunc.Input_Question = user_input

        start = time.time()
        Ai_response = Agent_Executor.invoke({"input": user_input})['output']
        end = time.time()

        print(f"\nTotal Query time: {end - start}")
        
        
        if not isinstance(Ai_response, str):
            if (Ai_response is None or len(Ai_response) == 0):
                result = '資料不存在'

            result = "完成資料搜尋"
        else:
            result = Ai_response

        return make_response(jsonify({'response': result}), 200, header)

    except Exception as e:
        result = "我不知道怎麼回答"
        print(f'\nThe error message is here: {e}')
    
    return make_response(jsonify({'response': result}), 200, header)

# 表格資料回傳
@app.route("/table")
def table():
    id = int(request.args.get('id'))
    if id > len(SummaryFunc.datasets)-1:
         id = len(SummaryFunc.datasets)-1

    try:
        header={
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET'
        }
        if SummaryFunc.datasets[id].empty:
            print(SummaryFunc.datasets[id])
            return make_response(jsonify([{"question":SummaryFunc.history[id], "data":[{"無欄位名稱": "無欄位資料"}], "count": SummaryFunc.count}]), 200, header)

        else:
            df = SummaryFunc.datasets[id].copy(deep=True)
            for column in df.dtypes[df.dtypes == 'datetime64[ns]'].index:
                df[column] = df[column].apply(lambda x: x.strftime("%Y-%m-%d"))

            json_data = df.to_json(orient='records')
            parsed = json.loads(json_data)

            return make_response(jsonify([{"question":SummaryFunc.history[id], "data": json_data, "count": SummaryFunc.count}]), 200, header)
    except Exception as e:
        print(str(e)+"\n")
        return make_response(jsonify([{"question":"無查詢紀錄", "data":[{"無欄位名稱": "無欄位資料"}], "count": SummaryFunc.count}]), 200, header)

# 彙總
@app.route('/get_summary')
def get_summary():
    
    header={
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET'
    }

    try:
        # result = SummaryFunc.query(user_input)
        start = time.time()
        # result = SummaryFunc.summary()
        result = "總結測試"
        end = time.time()

        print(f"\nTotal Summary time: {end - start}")

    except Exception as e:
        result = "我不知道怎麼回答"
        print(f'\nThe error message is here: {e}')

    return make_response(jsonify({'response': result}), 200, header)


# 上傳檔案
@app.route('/upload_doc', methods=['POST'])
@cross_origin()
def upload_documents():
    responses = []
    print(f'\nfile objects that I receive in this upload:{request.files}')
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request.'}), 400

    files = request.files.getlist('file')  # Get the list of files

    for file in files:
        print('\nthis file:', file)
        if file.filename == '':
            responses.append({'message': '''There's a bad file.''', 'code': 400})
        
        try:
            # Save the file to a temporary location with original extension
            temp_name = ''
            extension = os.path.splitext(file.filename)[-1].lower()
            if extension == ".csv":
                directory = "./database/File/"
                with open(directory+file.filename, 'w') as local_file:
                    file.save(local_file.name)
                    print("Saved file:", file.filename)

                with open(directory+"tables.txt", 'w') as file:
                    for csv in os.listdir(directory):
                        csv_name, csv_extentsion = csv.split('.')
                        if  csv_extentsion == "csv":
                            file.writelines(csv_name+" | "+", ".join(column for column in list(pd.read_csv(directory+csv, nrows=0).columns))+"\n")
                
                Agent_Executor = reload()

            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
                    temp_name = temp_file.name
                    file.save(temp_name)
                    print("Temporary file path:", temp_name)
                RetrievalQA.process_and_store_documents([temp_name])
                responses.append({
                    'message': f'File uploaded and processed successfully to Temporary space {temp_file.name}', 'code': 200
                })
        except Exception as e:
            app.logger.debug('Debug message')
            print(str(e))
        finally:
            # Delete the temporary file
            if temp_name:
                os.remove(temp_name)
    
    responses.append('end message:file upload successfully finished')
    return jsonify({'responses': responses}), 200


# RAG
@app.route('/get_qa', methods=['POST', 'OPTIONS'])
@cross_origin()
def get_qa():
    
    header={
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST'
    }
    data = request.get_json()
    print(f'server receive data from User input: {data}')
    user_input = data.get('inputText') #等同於 data['inputText']

    try:
        result = RetrievalQA.invoke(user_input)

    except Exception as e:
        result = "我不知道怎麼回答"
        print(f'\nThe error message is here: {e}')

    return make_response(jsonify({'response': result}), 200, header)

@app.after_request
def after_request(response):
    response.access_control_allow_origin = "*"
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5001)










