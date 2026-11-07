# Lindy Todo API

Lindy Todo is a small REST API for managing todo items. It is built with **FastAPI** and stores data in **PostgreSQL**. The API supports listing, creating, updating, and deleting todos.

## Project files

- `main.py` - Defines the FastAPI application, CORS configuration, PostgreSQL connection pool, request models, and todo API routes.
- `schema.sql` - Creates the PostgreSQL `todos` table used by the API.
- `requirements.txt` - Pins the Python packages required to run the application.
- `.env.example` - Template for the database connection settings. Copy it to `.env` and replace the example values.
- `.gitignore` - Prevents local Python files, virtual environments, editor files, and secrets in `.env` from being committed.

## Requirements

- Python 3.10 or newer
- PostgreSQL
- `pip`

## Recreate the setup

1. Clone the repository and enter it:

   ```bash
   git clone https://github.com/atiman-rohatgi/lindy_todo.git
   cd lindy_todo
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, use `.venv\\Scripts\\Activate.ps1` instead.

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a PostgreSQL database, then apply the schema:

   ```bash
   createdb todos
   psql -d todos -f schema.sql
   ```

   If your PostgreSQL setup requires a host or user, pass them to both commands as needed.

5. Create the environment file and configure it:

   ```bash
   cp .env.example .env
   ```

   Set `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` in `.env` to match your PostgreSQL database. Do not commit `.env`.

6. Start the development server:

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## API endpoints

- `GET /todos` - Return all todos.
- `POST /todos` - Create a todo. Example body: `{ "title": "Read the documentation" }`
- `PATCH /todos/{todo_id}` - Update completion status. Example body: `{ "completed": true }`
- `DELETE /todos/{todo_id}` - Delete a todo.

The current CORS configuration allows requests from `http://localhost:3000`, which is suitable for a local frontend. Update it before deploying a frontend at another origin.