import streamlit as st
from pathlib import Path
from sqlalchemy import create_engine
import sqlite3
import os

from langchain.agents import create_tool_calling_agent
from langchain.agents.agent_types import AgentType
from langchain.agents import initialize_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# Streamlit UI Setup
st.set_page_config(page_title="Langchain: Chat with SQL DB")
st.title("Langchain: Chat with SQL DB")

# Constants
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"
radio_opt = ["use sqlite3 Database - Student.db", "connect to your SQL Database"]

# Sidebar Input
selected_opt = st.sidebar.radio("Choose the DB you want to chat with", radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_url = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database Name")
else:
    db_url = LOCALDB

# API Key (Use secrets in production)
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.warning("Please provide the Groq API Key")
    st.stop()

# LLM Setup
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="Llama3-8b-8192",
    streaming=True,
)

@st.cache_resource(ttl="2h")
def configure_db(db_url, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_url == LOCALDB:
        db_file_path = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{db_file_path}?mode=ro", uri=True)
        engine = create_engine("sqlite://", creator=creator)
    elif db_url == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all required MySQL connection details.")
            st.stop()
        connection_url = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
        engine = create_engine(connection_url)
    else:
        st.error("Invalid database selection")
        st.stop()

    return SQLDatabase(engine)

# Configure DB
if db_url == MYSQL:
    db = configure_db(db_url, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_url)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
# Setup Toolkit and Agent
tools = toolkit.get_tools()
# agent_executor = create_tool_calling_agent(
#     llm=llm,
#     tools=toolkit.get_tools(),
#     prompt=SQL_FUNCTIONS_PROMPT
# )
# agent_executor = toolkit.get_agent()

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Session Message Setup
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

# Display past messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
user_query = st.chat_input("Ask anything from the database")
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("assistant"):
        callback_handler = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke({"input": user_query}, config={"callbacks": [callback_handler]})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
print("wcs")