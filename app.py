import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent #https://python.langchain.com/v0.1/docs/use_cases/sql/agents/
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

LOCALDB="USE_LOCALDB" ## sqllite3
MYSQL="USE_MYSQL"

radio_opt=["Use SQLLite 3 Database: office_llm.db","Connect to you MySQL Database"]

selected_opt=st.sidebar.radio(label="Choose the DB which you want to chat",options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Provide MySQL Host")
    mysql_user=st.sidebar.text_input("MYSQL User")
    mysql_password=st.sidebar.text_input("MYSQL password",type="password")
    mysql_db=st.sidebar.text_input("MySQL database")
else:
    db_uri=LOCALDB

## provide groq api key
api_key=st.sidebar.text_input(label="Groq API Key",type="password")

if not db_uri:
    st.info("Please enter the database information and uri")

if not api_key:
    st.info("Please add the groq api key")
if api_key:
    ## LLM model
    llm=ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)

    ## Configure the desired database and return the database object
    @st.cache_resource(ttl="2h") ## keep in cache for 2 hours
    def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
        print(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
        if db_uri==LOCALDB:
            dbfilepath=(Path(__file__).parent/"office_llm.db").absolute()
            print(dbfilepath)
            creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
            return SQLDatabase(create_engine("sqlite:///", creator=creator))
        elif db_uri==MYSQL:
            if not (mysql_host and mysql_user and mysql_password and mysql_db):
                st.error("Please provide all MySQL connection details.")
                st.stop()
            mysql_password = mysql_password.replace('@','%40') # if @ is there in password
            print(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")
            return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))   
        
    if db_uri==MYSQL:
        db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
    else:
        db=configure_db(db_uri) ## no info required for sqllite

    ## SQL database toolkit
    toolkit=SQLDatabaseToolkit(db=db,llm=llm)

    ## AGENT
    agent=create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

    if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
        st.session_state["messages"] = [{"role": "assistant", 
                                        "content": "How can I help you?"}]

    ## appending so that it has all message info - history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_query=st.chat_input(placeholder="Ask anything from the database")

    if user_query:
        st.session_state.messages.append({"role": "user", 
                                        "content": user_query})
        st.chat_message("user").write(user_query)

        with st.chat_message("assistant"):
            streamlit_callback=StreamlitCallbackHandler(st.container()) ## show chain of thoughts of agent
            response=agent.run(user_query,callbacks=[streamlit_callback])
            st.session_state.messages.append({"role":"assistant","content":response})
            st.write(response)

            


