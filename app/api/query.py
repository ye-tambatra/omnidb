from fastapi import APIRouter, HTTPException
from app.models import QueryRequest, QueryResponse
from app.agent import create_omni_agent
from app.database import get_configured_db_url
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/query", response_model=QueryResponse)
async def execute_query(payload: QueryRequest):
    db_url = get_configured_db_url()
    if not db_url:
        raise HTTPException(status_code=400, detail="Target database URL is not configured. Please configure it first via /config/db_url endpoint.")
        
    try:
        agent_executor = create_omni_agent(db_url=db_url, permission_level=payload.permission_level)
        
        # Invoke agent
        response = agent_executor.invoke({"input": payload.query})
        
        return QueryResponse(
            explanation=response.get("output", "No output provided."),
            raw_data=None  # Extended version could parse out agent steps to map raw tool responses here
        )
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong, Please try again later.")
