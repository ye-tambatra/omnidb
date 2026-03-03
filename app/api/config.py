from fastapi import APIRouter, HTTPException
from app.models import DbUrlUpdateRequest, DbUrlResponse, PermissionLevelUpdateRequest, PermissionLevelResponse
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

@router.get("/config/permission_level", response_model=PermissionLevelResponse)
def get_permission_level():
    """Retrieve the current global permission level."""
    level = get_setting("current_permission_level")
    return {"level": int(level) if level else 1}

@router.put("/config/permission_level")
def update_permission_level(payload: PermissionLevelUpdateRequest):
    """Update the global permission level."""
    from app.config_db import get_all_permissions
    
    valid_levels = [p["level"] for p in get_all_permissions()]
    if payload.level not in valid_levels:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid permission level. Valid levels are: {valid_levels}"
        )
        
    set_setting("current_permission_level", str(payload.level))
    return {"status": "success", "message": f"Global permission level updated to {payload.level}."}
