# https://sandeep14.medium.com/running-graphrag-locally-with-neo4j-and-ollama-text-format-371bf88b14b7

import os
import time
from fastapi import FastAPI, HTTPException
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from langchain_community.graphs import Neo4jGraph
from langchain_community.chat_models import ChatOllama
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.vectorstores import Neo4jVector
from langchain_core.documents import Document
# from langchain_ollama import OllamaEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_experimental.llms.ollama_functions import OllamaFunctions

from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import time


graph = Neo4jGraph(
    url= "bolt://localhost:7687" ,
    username="neo4j", #default
    password="12345678" #change accordingly
)

# text = """
# Marie Curie, born in 1867, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.
# She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
# Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
# She was, in 1906, the first woman to become a professor at the University of Paris. 
# """

#========================Ingestion==========================

# loader = DirectoryLoader('C:/Users/fintechdev05.bank/Downloads/好市多介紹', glob="**/*.docx", loader_cls=Docx2txtLoader)
loader = Docx2txtLoader("C:/Users/fintechdev05.bank/Downloads/好市多介紹/Costco介紹.docx")
docs = loader.load()
print(len(docs))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30,
)
documents = text_splitter.split_documents(docs)

# Convert the text into documents
# documents = [Document(page_content=text)]

# Initialize the language model for text-to-graph conversion
system_prompt = (
    "# Knowledge Graph Instructions\n"
    "## 1. Overview\n"
    "You are a top-tier algorithm designed for extracting information in structured "
    "formats to build a knowledge graph.\n"
    "Try to capture as much information from the text as possible without "
    "sacrificing accuracy. Do not add any information that is not explicitly "
    "mentioned in the text.\n"
    "- **Nodes** represent entities and concepts.\n"
    "- The aim is to achieve simplicity and clarity in the knowledge graph, making it\n"
    "accessible for a vast audience.\n"
    "## 2. Labeling Nodes\n"
    "- **Consistency**: Ensure you use available types for node labels.\n"
    "Ensure you use basic or elementary types for node labels.\n"
    "- For example, when you identify an entity representing a person, "
    "always label it as **'person'**. Avoid using more specific terms "
    "like 'mathematician' or 'scientist'."
    "- **Node IDs**: Never utilize integers as node IDs. Node IDs should be "
    "names or human-readable identifiers found in the text.\n"
    "- **Relationships** represent connections between entities or concepts.\n"
    "Ensure consistency and generality in relationship types when constructing "
    "knowledge graphs. Instead of using specific and momentary types "
    "such as 'BECAME_PROFESSOR', use more general and timeless relationship types "
    "like 'PROFESSOR'. Make sure to use general and timeless relationship types!\n"
    "## 3. Coreference Resolution\n"
    "- **Maintain Entity Consistency**: When extracting entities, it's vital to "
    "ensure consistency.\n"
    'If an entity, such as "John Doe", is mentioned multiple times in the text '
    'but is referred to by different names or pronouns (e.g., "Joe", "he"),'
    "always use the most complete identifier for that entity throughout the "
    'knowledge graph. In this example, use "John Doe" as the entity ID.\n'
    "Remember, the knowledge graph should be coherent and easily understandable, "
    "so maintaining consistency in entity references is crucial.\n"
    "## 4. Strict Compliance\n"
    "Adhere to the rules strictly. Non-compliance will result in termination."
)

self_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt,
        ),
        (
            "human",
            (
                "Tip: Make sure to answer in the correct format and do "
                "not include any explanations. "
                "Use the given format to extract information from the "
                "following input: {input}"
            ),
        ),
    ]
)
llm = ChatOllama(model="mistral-nemo", temperature=0)
llm_transformer_filtered = LLMGraphTransformer(llm=llm)

# Convert the text into graph documents

t1 = time.time()
graph_documents = llm_transformer_filtered.convert_to_graph_documents(documents)
t2 = time.time()
print('time elapsed: ' + str(t2-t1) + ' seconds')

# Add the generated graph into Neo4j
graph.add_graph_documents(
    graph_documents,
    baseEntityLabel=True,
    include_source=True
)

# Optional: Create embeddings for more complex search queries

# embed = OllamaEmbeddings(model="aerok/zpoint_large_embedding_zh") # mxbai-embed-large
# vector_index = Neo4jVector.from_existing_graph(
#     embedding=embed,
#     search_type="hybrid",
#     node_label="Document",
#     text_node_properties=["text"],
#     embedding_node_property="embedding",
#     url= "bolt://localhost:7687",
#     username="neo4j", #default
#     password="12345678" #change accordingly
# )
# vector_retriever = vector_index.as_retriever()

#========================querying_neo4j==========================
# print("stage - querying_neo4j")

# # Define a model for the extracted entities from the text
# class Entities(BaseModel):
#     names: list[str] = Field(..., description="All entities from the text")

# # Define a prompt to extract entities from the input query
# prompt = ChatPromptTemplate.from_messages([ 
#     ("system", "Extract organization and person entities from the text."),
#     ("human", "Extract entities from: {question}")
# ])

# # Initialize the Ollama model for entity extraction with LLM (using "gemma2")
# llm = OllamaFunctions(model="gemma2", format="json", temperature=0)

# # Combine the prompt and LLM to create an entity extraction chain
# # The output is structured to match the "Entities" model
# entity_chain = prompt | llm.with_structured_output(Entities, include_raw=True)

# # Function to retrieve relationships of the extracted entities from Neo4j
# def graph_retriever(question: str) -> str:
#     # Use the entity extraction chain to get entities from the question
#     response = entity_chain.invoke({"question": question})
#     # Extract the list of entity names from the response
#     entities = response['raw'].tool_calls[0]['args']['names']
#     print("Retreived Entities")
#     print(response)
#     result = ""  # Initialize a variable to store the result

#     # Iterate over each extracted entity
#     for entity in entities:
#         # Query Neo4j to get relationships for the given entity
#         query_response = graph.query(
#             """MATCH (p:Person {id: $entity})-[r]->(e)
#             RETURN p.id AS source_id, type(r) AS relationship, e.id AS target_id
#             LIMIT 50""",
#             {"entity": entity}
#         )
#         # Format the query results and append to the result string
#         result += "\n".join([f"{el['source_id']} - {el['relationship']} -> {el['target_id']}" for el in query_response])
    
#     # Return the formatted results containing entity relationships
#     return result

# #========================querying_ollama==========================
# print("stage - querying_ollama")
# # Define a function that combines data retrieved from both Neo4j and vector embeddings
# def full_retriever(question: str):
#     # Retrieve graph data for the question using the graph_retriever function
#     graph_data = graph_retriever(question)
#     print("Graph Data")
#     print(graph_data)
#     # Retrieve vector data by invoking the vector retriever with the question
#     vector_data = [el.page_content for el in vector_retriever.invoke(question)]
    
#     # Combine the graph data and vector data into a formatted string
#     return f"Graph data: {graph_data}\nVector data: {'#Document '.join(vector_data)}"

# # Define a prompt template for generating a response based on context
# template = """Answer the question based only on the following context:
# {context}
# Question: {question}
# Answer:"""

# # Create a prompt from the template, which takes the context and question as input
# prompt = ChatPromptTemplate.from_template(template)

# # Create a processing chain that:
# # 1. Generates context using the full_retriever function
# # 2. Passes through the question as-is using RunnablePassthrough
# # 3. Applies the prompt template to generate the final question
# # 4. Uses the LLM (language model) to generate the answer
# # 5. Uses StrOutputParser to format the output as a string
# chain = (
#     {
#         "context": lambda input: full_retriever(input),  # Generate context from the question
#         "question": RunnablePassthrough(),  # Pass the question through without modification
#     }
#     | prompt  # Apply the prompt template
#     | llm  # Use the language model to answer the question based on context
#     | StrOutputParser()  # Parse the model's response as a string
# )

# # Test the chain with a question
# response = chain.invoke(input="Who are Marie Curie and Pierre Curie?")
# print("Final Answer")
# print(response)
