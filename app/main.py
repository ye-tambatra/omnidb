import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Load env variables 
load_dotenv()

from app.api.query import router as query_router
from app.api.permissions import router as permissions_router
from app.api.config import router as config_router
from app.config_db import init_config_db

# Initialize SQLite configuration db
init_config_db()

app = FastAPI(
    title="OmniDB",
    description="Plug-and-play FastAPI service translating natural language to SQL with granular safety permissions.",
    version="1.0.0"
)

app.include_router(query_router, tags=["Query"])
app.include_router(permissions_router, tags=["Permissions"])
app.include_router(config_router, tags=["Config"])

@app.get("/")
def health_check():
    return {"status": "running", "message": "OmniDB is up."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
