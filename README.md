# OmniDB

Welcome to **OmniDB**! 

Have you ever wished you could just *talk* to your database instead of writing complex SQL queries? OmniDB is a plug-and-play FastAPI service designed to do exactly that. 

It acts as a smart middleware that connects to essentially *any* SQL database and uses AI to translate your natural language requests directly into database actions. Need to know *"How many users signed up today?"* or *"Give me the titles of all posts made by Alice"*? Just ask. 

OmniDB manages the database connection dynamically and wraps every query in a robust safety permission guard.

## What It's For

OmniDB is built for developers who want to quickly expose a natural language interface for their databases—without blindly executing dangerous operations. We abstract away the entire SQL generation loop so you can elegantly plug OmniDB into a chatbot UI, an admin dashboard, or your internal tools right out of the box.

## Core Features

- **Natural Language to SQL**: Translates human sentences into properly formatted and schema-aware SQL operations instantly.
- **Dynamic Target Configuration**: Manage your target database connection purely via an API endpoint. You can dynamically swap which database the app is investigating.
- **Granular Permission Guard**: Protects your database against rogue operations. Strict permission levels (Read-Only, Data Entry, and Full Admin) intercept and validate the generated SQL commands *before* they are sent to your database.
- **Self-Hosted Configuration**: Uses an embedded SQLite database to persist your application settings locally (like current permission levels and active target databases) so they persist between server reboots.

## Tech Stack

- **Framework**: FastAPI (for lightning-fast API magic)
- **AI/LLM**: LangChain & Google GenAI (`gemini-2.5-flash`)
- **Database Toolkit**: SQLAlchemy (enabling support for Postgres, MySQL, SQLite, SQL Server, etc.)
- **Configuration Store**: Local SQLite database (`omnidb_config.sqlite`)

## Setup Instructions

1. **Environment Setup**
   Ensure you have Python 3 installed. Create and activate a virtual environment inside the project directory:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**
   Install all the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set API Credentials**
   OmniDB needs to talk to Google's Gemini LLM to interpret your language. Create an `.env` file referencing the given example:
   ```bash
   cp .env.example .env
   ```
   Open the new `.env` file and assign your API Key to `GOOGLE_API_KEY`.

4. **Run the Application!**
   Boot up the API server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The fully interactive API documentation will now be available in your browser at [http://localhost:8000/docs](http://localhost:8000/docs).

## Available Endpoints

### Configuration
- `GET /config/db_url`: Check which target database OmniDB is currently interrogating.
- `PUT /config/db_url`: Point OmniDB to a new database. *(Automatically validates the connection on the fly!)*
- `GET /config/permission_level`: Preview the currently active safety level.
- `PUT /config/permission_level`: Safely switch behavior bounds. Setting Level `1` strictly permits SELECT reads, whereas Level `3` empowers the AI with full DDL/DML editing capabilities.

### Execution
- `POST /query`: The core engine. Send your natural language text snippet to OmniDB. The agent will survey your active schema, formulate a safe SQL query, execute it, and respond with a clean, conversational explanation of the results.
