import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

from prompts import final_prompt, answer_prompt

from operator import itemgetter

db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")

@st.cache_resource
def get_chain():
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    table_info = db.get_table_info()
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    
    generate_query = create_sql_query_chain(llm, db,final_prompt.partial(top_k=2))
    
    execute_query = QuerySQLDatabaseTool(db=db)
    
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    
    chain = (
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
    )
    
    return chain

def create_history(messages):
    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history

def invoke_chain(question,messages):
    chain = get_chain()
    history = create_history(messages)
    response = chain.invoke({"question": question,"messages":history.messages})
    history.add_user_message(question)
    history.add_ai_message(response)
    return response