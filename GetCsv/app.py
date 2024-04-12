from flask import Flask, request, render_template
from flask_cors import CORS
from getCustomerDataset import  getCsvDataset
from DataVisualization import DataVisualization
import time


def get_dataset(filename="./客戶業績資料表.csv"):
    return getCsvDataset.getCsvDataset(filename)

def get_data(filename="./客戶業績資料表.csv", query = None):
    return getCsvDataset.dataset_query(filename, query)

def get_data_sql(filename="./客戶業績資料表.csv", query = None):
    return getCsvDataset.dataset_query_sql(filename, query)

def get_plot(data):
    DataVisualization.lineplot(data)
    

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/all")
def get_all_data():
    dataset = get_dataset()
    if (dataset is None or len(dataset) == 0):
        return '資料不存在', 404

    return dataset.to_dict(orient='records')

@app.route("/search")
def search():
    query = {
        "E_name" : request.args.get('e_name'),
        "C_name" : request.args.get('c_name'),
        "E_ID" : request.args.get('e_id'),
        "C_ID" : request.args.get('c_id'),
        "Start_date" : request.args.get('date_start'),
        "End_date" : request.args.get('date_end'),
        "P_name" : request.args.get('p_name'),
        "T_amount" : request.args.get('t_amount'),
        "OrderBy" : 1
        }

    data = get_data(query = query)
    if (data is None or len(data) == 0):
        return '資料不存在', 404
    else:
        get_plot(data)
        print("test: " + data.to_dict(orient='records')[0]["Employee_Name"])
        return render_template('table.html', dataset=data.to_dict(orient='records'))
#    return data.to_dict(orient='records')

@app.route("/search2")
def search2():
    
    query = "SELECT Employee_Name, Sum(Transaction_Amount) FROM dataset GROUP BY Employee_Name"

    data = get_data_sql(query = query)
    
    if (data is None or len(data) == 0):
        return '資料不存在', 404
    
    return render_template('table.html', dataset=data.to_dict(orient='records'))
    


@app.after_request
def after_request(response):
    response.access_control_allow_origin = "*"
    return response

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5001)











