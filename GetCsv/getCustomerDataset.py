import pandas as pd
import duckdb
import time
import re
import os
from langchain_core.prompts import ChatPromptTemplate

from config import Infom

# from Langchain_Agent import Agent_Executor, refineSQL

# dtype={
#                     'Transaction_ID': 'string',
#                     'Employee_ID': 'string',
#                     'Employee_Name': 'string',
#                     'Transaction_Date': 'int64',
#                     'Product_Name': 'string',
#                     'Transaction_Amount': 'int64',
#                     'Customer_ID': 'string',
#                     'Customer_Name': 'string',
# }

def multi_query(text):
    query_text = ""
    
    for s in text.split(","):
        query_text += (f"'{s}',")

    return query_text[:-1]

def isAvailable():
    return Infom["Authentication"]["search_csv"]

def refineQuery(query=None):
        pattern1 = r"SELECT [^()] FROM"
        pattern2 = r"FROM\s+\S+"
        pattern3 = r"FROM .* WHERE"

        replacement1 = "SELECT * FROM"
        replacement2 = "FROM dataTable"
        replacement3 = "FROM dataTable WHERE"

        query = query.replace("\n"," ")

        if ("DISTINCT" not in query):
            # query = re.sub(pattern1, replacement1, query)
            pass

        query = re.sub(pattern2, replacement2, query)
        # query = re.sub(pattern3, replacement3, query)

        return query

def refineSQL(llm = None, query = None, column_names=None, error=''):
    # refer to this error message: {error}.
    system = f'''
     Follow the rules:
        1. Replace the relative field names used in SQL Commmand by {column_names}.
        2. Remove the field names that are not in {column_names} or '*'.
        3. Give the date data like 20240101, not '2024-01-01' 

        Return only SQL Command, and the format must be like 'SELECT ... FROM ... WHERE ...'.

    '''

    human = '''{input}

        (reminder to respond only a SQL Command)'''

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", human),
        ]
    )
    print("Refining ...")
    # result = llm.invoke(prompt.format(input=query))
    return llm.invoke(prompt.format(input=query))

class getCsvDataset:
    def __init__(self):
        self.filename = filename
        
    def dataset_query_sql(repo, llm, query):
        
        try:
            if not isAvailable():
                return "您沒有權限"

            files = os.listdir(repo)
            
            for i, file in enumerate(files):

                filename = file.split(".")[0]
                # print(filename)
                if filename in query:
                    temp = pd.read_csv(repo+"/"+file, encoding='utf-8')
                    if 'Transaction_Date' in temp.columns:
                        temp['Transaction_Date'] = pd.to_datetime(temp['Transaction_Date'], format="%Y%m%d")
                        temp['Transaction_Date'] = temp['Transaction_Date'].apply(lambda x: x.strftime("%Y-%m-%d"))
                    locals()[f"table{i}"] = temp
                    query = query.replace(filename, f"table{i}")
                    
            query = query[query.find('SELECT'): query.find(';')]

            print("final query: \n"+query)

            # query = refineQuery(query)
            # print("Refined Query: "+query)
            return duckdb.query(query).df()
            # try:
            #     return duckdb.query(query).df()

            # except:
            #     return "我不知道怎麼回答"
                # query = refineSQL(llm, query, (", ".join(list(dataTable.columns.values))))
                # print("Refined Query: "+query)

                # query = refineQuery(query)
                # query = re.search(r"SELECT .*", query).group().replace("```","")
                # # query = refineQuery(query)
                # print("Final: "+query)

                # return duckdb.query(query).df()
            
        
        except FileNotFoundError as error:
            
            print("檔案不存在")
            return None
    

if __name__ == "__main__":
    
    print(getCsvDataset.getCsvDataset("./客戶業績資料表.csv"))
    
        
            
    
