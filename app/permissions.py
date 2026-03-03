import re
from pydantic import BaseModel, Field
from typing import Type, Any
from langchain_core.tools import BaseTool

from app.config_db import get_allowed_operations

class GuardedQueryInput(BaseModel):
    query: str = Field(description="A detailed and correct SQL query to execute.")

class GuardedQuerySQLDatabaseTool(BaseTool):
    """Tool for querying a SQL database, wrapped with permission checks."""
    name: str = "sql_db_query_guarded"
    description: str = """
    Execute a SQL query against the database and get back the result.
    If the query is not correct or not permitted, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """
    args_schema: Type[BaseModel] = GuardedQueryInput
    
    db: Any # Needs to be SQLDatabase
    permission_level: int
    
    def _run(self, query: str) -> str:
        # Fetch allowed operations from SQLite
        allowed = get_allowed_operations(self.permission_level)
        if not allowed:
            return f"Error: Permission level {self.permission_level} has no allowed operations or does not exist."
            
        all_commands = ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "INSERT", "UPDATE", "DELETE", "ALTER", "DROP", "CREATE", "TRUNCATE", "REPLACE"]
        q_upper = query.upper()
        
        found_commands = [cmd for cmd in all_commands if re.search(rf'\b{cmd}\b', q_upper)]
        
        for cmd in found_commands:
            if cmd not in allowed:
                return f"Error: Safety violation. Command '{cmd}' is not allowed for Permission Level {self.permission_level}."
        
        # If safe, execute using standard logic
        try:
            return self.db.run(query)
        except Exception as e:
            return f"Error executing query: {str(e)}"
