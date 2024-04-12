import pandas as pd
import duckdb

dtype={
                    'Transaction_ID': 'string',
                    'Employee_ID': 'string',
                    'Employee_Name': 'string',
                    'Transaction_Date': 'int64',
                    'Product_Name': 'string',
                    'Transaction_Amount': 'int64',
                    'Customer_ID': 'string',
                    'Customer_Name': 'string',
}
def multi_query(text):
    query_text = ""
    
    for s in text.split(","):
        query_text += (f"'{s}',")

    return query_text[:-1]
    
    

class getCsvDataset:
    def __init__(self):
        self.filename = filename
    
    def getCsvDataset(filename):
        try:
            dataset = pd.read_csv(filename, dtype=dtype)

            return dataset
        
        except FileNotFoundError as error:
            
            print("檔案不存在")
            return None
        
    def dataset_query(filename, query):
        
        try:
            dataset = pd.read_csv(filename, dtype=dtype)
            if (query["E_ID"]):
                dataset = dataset.query(f"Employee_ID == '{query["E_ID"]}'")
            if ("," in query["E_name"]):
                dataset = dataset.query(f"Employee_Name in ({multi_query(query["E_name"])})")
            elif (query["E_name"]):
                dataset = dataset.query(f"Employee_Name == '{query["E_name"]}'")
            if (query["C_ID"]):
                dataset = dataset.query(f"Customer_ID == '{query["C_ID"]}'")            
            if ("," in query["C_name"]):
                dataset = dataset.query(f"Customer_Name in ({multi_query(query["C_name"])})")
            elif (query["C_name"]):
                dataset = dataset.query(f"Customer_Name == '{query["C_name"]}'")
                
            if (query["Start_date"] and query["End_date"]):
                dataset = dataset.query(f"{int(query["Start_date"])} <= Transaction_Date <= {int(query["End_date"])}")
            elif (query["Start_date"]):
                dataset = dataset.query(f"{int(query["Start_date"])} <= Transaction_Date")
            elif (query["End_date"]):
                dataset = dataset.query(f"Transaction_Date <= {int(query["End_date"])}")

            if (query["P_name"]):
                dataset = dataset.query(f"Product_Name == '{query["P_name"]}'")
            try:
                if (">=" in query["T_amount"]):
                    dataset = dataset.query(f"Transaction_Amount >= {int(query["T_amount"][2:])}")
                elif ("<=" in query["T_amount"]):
                    dataset = dataset.query(f"Transaction_Amount <= {int(query["T_amount"][2:])}")
                elif (">" in query["T_amount"]):
                    dataset = dataset.query(f"Transaction_Amount > {int(query["T_amount"][1:])}")
                elif ("<" in query["T_amount"]):
                    dataset = dataset.query(f"Transaction_Amount < {int(query["T_amount"][1:])}")
                elif (query["T_amount"]):
                    dataset = dataset.query(f"Transaction_Amount == {int(query["T_amount"])}")
            except ValueError as error:
                return None
            
            if(query["OrderBy"]):
                dataset = dataset.sort_values(by=['Employee_Name', 'Transaction_ID'], ascending=True)
                    
                
            return dataset
        
        except FileNotFoundError as error:
            
            print("檔案不存在")
            return None
        
    def dataset_query_sql(filename, query):
        
        try:
            dataset = pd.read_csv(filename, dtype=dtype)

            return duckdb.query(query).df()
        
        except FileNotFoundError as error:
            
            print("檔案不存在")
            return None

if __name__ == "__main__":
    
    print(getCsvDataset.getCsvDataset("./客戶業績資料表.csv"))
    
        
            
    
