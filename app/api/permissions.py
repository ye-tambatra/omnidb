from fastapi import APIRouter, HTTPException
from typing import List
from app.models import PermissionConfig, PermissionUpdateRequest
from app.config_db import get_all_permissions, update_allowed_operations

router = APIRouter()

@router.get("/permissions", response_model=List[PermissionConfig])
def list_permissions():
    """List all available permission levels and their allowed operations."""
    return get_all_permissions()

@router.put("/permissions/{level}", response_model=dict)
def update_permission(level: int, payload: PermissionUpdateRequest):
    """Update allowed operations for a specific permission level."""
    try:
        update_allowed_operations(level, payload.allowed_operations)
        return {"status": "success", "message": f"Updated permission level {level}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
