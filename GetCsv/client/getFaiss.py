import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama

from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.document_loaders import Docx2txtLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_core.prompts import ChatPromptTemplate

from pathlib import Path
import os



class getFAISS:
    def __init__(self, llm):
        self.embeddings = OllamaEmbeddings(model="shaw/dmeta-embedding-zh")
        self.llm = llm
        # self.llm = Ollama(model = "yabi/breeze-7b-32k-instruct-v1_0_q6_k", temperature = 0)

        current_script_path = Path(__file__).resolve().parent
        self.faiss_index_path = current_script_path / 'faiss_index'
        self.faiss_index_path.mkdir(parents=True, exist_ok=True)
        self.index_path = self.faiss_index_path / 'index.faiss'

        # if not index_path.exists():
        #     texts = ['這是一個測試文本', '這是另一個測試文本']
        #     db = FAISS.from_texts(texts, self.embeddings)
        #     db.save_local(folder_path=str(self.faiss_index_path))

    def process_and_store_documents(self, file_paths) -> None:
        
        doc_chunks = []
        chunkSize = 500

        for file_path in file_paths:
            extension = os.path.splitext(file_path)[-1].lower()  # Get the file extension

            if extension == '.txt':
                loader = TextLoader(file_path, autodetect_encoding=True)

            elif extension == '.csv':
                loader = CSVLoader(file_path)

            elif extension == '.xlsx':
                loader = UnstructuredExcelLoader(file_path,mode="elements")

            elif extension == '.pdf':
                loader = PDFPlumberLoader(file_path)

            elif extension == '.docx':
                loader = Docx2txtLoader(file_path)

            else:
                loader = UnstructuredFileLoader(file_path)
            
            documents = loader.load_and_split() if extension == '.pdf' else loader.load()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunkSize, chunk_overlap=50, separators=["\n", "\n\n", "\t", "。"]
            )
            split_docs= text_splitter.split_documents(documents)  
            doc_chunks.extend(split_docs)
        
        faiss_path = str(self.faiss_index_path)

        if not self.index_path.exists():
            docsearch = FAISS.from_documents(doc_chunks, self.embeddings)
            docsearch.save_local(folder_path=faiss_path)
        else:
            # 加載FAISS
            docsearch = FAISS.load_local((faiss_path), self.embeddings, allow_dangerous_deserialization=True)
            new_metadatas = [doc.metadata for doc in doc_chunks]
            # 提取每個文檔的實際來源
            docsearch.add_texts([t.page_content for t in doc_chunks], metadatas=new_metadatas)
            docsearch.save_local(folder_path=faiss_path)

    def getData(self, query):

        faiss_path = str(self.faiss_index_path)
        docsearch = FAISS.load_local((faiss_path), self.embeddings, allow_dangerous_deserialization=True)
        retriever=docsearch.as_retriever(search_kwargs={'k': 3})
        print(docsearch.similarity_search_with_score(query))
        docs = retriever.invoke(query)


        json_serializable_doc = {
            'page_content': [doc.page_content for doc in docs],
            'metadata': [doc.metadata for doc in docs]
        }

        self.Content = ""

        for doc in docs:
            self.Content = self.Content + f"{doc.page_content} \n "
        
        # {doc.metadata if doc.metadata else 'No Metadata'} \n
            
    # 影響結果的參數: chunk size=500, overlap=50, top_K=3
    def invoke(self, msg):
            try:
                self.getData(msg)
                # Below DOCUMENT is for query.
                # ===DOCUMENT START===
                # {self.Content}
                # ===DOCUMENT END===

                # ===
                # Thought: Do I need to answer using contents? Do user ask a question or not?
                # Action:
                # If DO, merge the content as answer, then respond naturally, like a person. 
                # If DO NOT, don't say anything about DOCUMENT, just respond naturally.
                # ===

                # Begin! 
                # Here is user input.

                system = f'''
                    這是參考文件
                    # ===文件開始===
                    # {self.Content}
                    # ===文件結束===

                    思考：我需要用參考文件的內容來回答問題嗎？ 用戶有問任何問題嗎？
                    動作：
                    如果有，將文件中相關內容作為答案，並自然地回覆
                    如果沒有，不要說任何跟文件相關的內容，並自然地回覆

                    開始！
                    接下來是用戶的輸入。
                    '''


                human = '''{input}|只用繁體中文回覆
                    '''

                prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", system),
                        ("human", human),
                    ]
                )
                print("Thinking ...")

                result = self.llm.invoke(prompt.format(input=msg))
                print("result: "+result)

                return result

            except Exception as e:
                print(str(e))
                return "無法查詢"


if __name__ == '__main__':

    # 獲取當前 Python 腳本的絕對路徑
    current_script_path = Path(__file__).resolve().parent

    # 在當前目錄下檢查 "faiss_index" 資料夾是否存在
    faiss_index_path = current_script_path / 'faiss_index'
    faiss_index_path.mkdir(parents=True, exist_ok=True)
    # 檢查 "index.faiss" 文件是否存在
    index_path = faiss_index_path / 'index.faiss'

    # 讀取已經創建的向量數據庫
    index = faiss.read_index(str(index_path))
    # 獲取向量數據庫中的向量數量
    num_vectors = index.ntotal
    print("向量數據庫中的向量數量：", num_vectors)
