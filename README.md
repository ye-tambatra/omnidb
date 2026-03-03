# OmniDB

OmniDB is a plug-and-play FastAPI service that transforms any SQL database URL into a natural language interface with granular safety permissions. It uses LangChain alongside Google Gemini 2.5 Flash to automatically interpret your intent and perform actions on your database based on granular permission layers. 

## Setup

1. **Environment Setup**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Keys**
   Set your Google Generative AI API key in a `.env` file or export it.
   ```bash
   export GOOGLE_API_KEY="your-gemini-key"
   ```

3. **Run**
    ```bash
    python -m app.main
    ```
    Or use `uvicorn app.main:app --reload`

## Architecture Highlights
- API Layer wrapped with `FastAPI`
- SQlite database for self-hosted dynamic permissions.
- Modularized Langchain integration for tool-calling capabilities.

## Endpoints

- `POST /query`: Translate natural language into a database execution response.
- `GET /permissions`: Check the configured permission levels.
- `PUT /permissions/{level}`: Update a given permission level's allowed commands dynamically.
