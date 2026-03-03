from pydantic import BaseModel, Field
from typing import Optional, Any

class QueryRequest(BaseModel):
    query: str = Field(..., description="The natural language question or request.")
    permission_level: int = Field(1, description="The permission level to enforce (1: Read-Only, 2: Data Entry, 3: Full Admin).")

class DbUrlUpdateRequest(BaseModel):
    db_url: str = Field(..., description="The SQLAlchemy database URL to connect to.")

class DbUrlResponse(BaseModel):
    db_url: Optional[str]

class QueryResponse(BaseModel):
    explanation: str = Field(..., description="The LLM's natural language explanation.")
    raw_data: Optional[Any] = Field(None, description="The raw data returned by the final SQL query (if applicable).")

class PermissionConfig(BaseModel):
    level: int
    name: str
    allowed_operations: str

class PermissionUpdateRequest(BaseModel):
    allowed_operations: str = Field(..., description="Comma-separated list of allowed SQL operations (e.g. 'SELECT,SHOW').")
