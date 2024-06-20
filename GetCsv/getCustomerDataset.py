import pandas as pd
import duckdb
import time
import re
import os
from langchain_core.prompts import ChatPromptTemplate

from config import Infom

def isAvailable():
    return Infom["Authentication"]["search_csv"]

class getCsvDataset:
    def __init__(self):
        pass
        
    def dataset_query_sql(repo, query):
        
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
                        # temp['Transaction_Date'] = temp['Transaction_Date'].apply(lambda x: x.strftime("%Y-%m-%d"))
                    locals()[f"table{i}"] = temp
                    query = query.replace(filename, f"table{i}")
                    print(f"table{i} = {filename}\n")
                    
            query = query[query.find('SELECT'): query.find(';')]

            print("final query: \n"+query)

            return duckdb.query(query).df()
        
        except FileNotFoundError as error:
            
            print("檔案不存在")
            return None
    

if __name__ == "__main__":
    
    pass
    
        
            
    
