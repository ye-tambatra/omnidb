from fastapi import APIRouter, HTTPException
from app.models import DbUrlUpdateRequest, DbUrlResponse
from app.config_db import get_setting, set_setting
from app.database import validate_db_connection

router = APIRouter()

@router.get("/config/db_url", response_model=DbUrlResponse)
def get_db_url():
    """Retrieve the current configured target database URL."""
    db_url = get_setting("target_db_url")
    return {"db_url": db_url}

@router.put("/config/db_url")
def update_db_url(payload: DbUrlUpdateRequest):
    """Set and validate a new target database URL."""
    if not validate_db_connection(payload.db_url):
        raise HTTPException(
            status_code=400, 
            detail="Database connection failed. URL is invalid or database is unreachable."
        )
    
    set_setting("target_db_url", payload.db_url)
    return {"status": "success", "message": "Target database URL updated successfully."}
