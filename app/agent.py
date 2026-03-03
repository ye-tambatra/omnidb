import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_community.tools.sql_database.tool import InfoSQLDatabaseTool, ListSQLDatabaseTool
from app.database import get_db
from app.permissions import GuardedQuerySQLDatabaseTool

def create_omni_agent(db_url: str, permission_level: int):
    # Instantiate DB
    db = get_db(db_url)
    
    # Instantiate LLM
    llm_model = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    llm = ChatGoogleGenerativeAI(model=llm_model, temperature=0)
    
    # Create Tools
    list_tool = ListSQLDatabaseTool(db=db)
    info_tool = InfoSQLDatabaseTool(db=db)
    query_tool = GuardedQuerySQLDatabaseTool(db=db, permission_level=permission_level)
    
    tools = [list_tool, info_tool, query_tool]
    
    # Construct prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct SQL query to run, then look at the results of the query and return the answer.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You must double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
        
        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database unless explicitly requested.
        Your permission level determines if you can make them.
        
        If you are provided with raw JSON data output as part of your answer, factor it into your response explanation.
        """),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor
