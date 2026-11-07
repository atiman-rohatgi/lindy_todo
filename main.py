import os
import psycopg2
from psycopg2 import pool
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"], #if in production, change to ["GET", "POST", "PUT", "DELETE"] or whatever methods you need
    allow_headers=["*"],
)

try:
    connection_pool = pool.SimpleConnectionPool(
        1, 10,
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
except Exception as e:
    raise RuntimeError(f"Failed to connect to the database at startup: {e}")

def get_conn():
    conn = connection_pool.getconn()
    try:
        yield conn
    finally:
        connection_pool.putconn(conn)

class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    completed: bool

@app.get("/todos", status_code=200)
def get_todos(conn=Depends(get_conn)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, completed FROM todos")
    rows = cursor.fetchall()
    return [{"id": str(row[0]), "title": row[1], "completed": row[2]} for row in rows]

@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate, conn=Depends(get_conn)):
    if not todo.title or not todo.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO todos (title, completed) VALUES (%s, %s) RETURNING id, title, completed",
        (todo.title.strip(), False)
    )
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=500, detail="Failed to create todo")
    conn.commit()
    return {"id": str(row[0]), "title": row[1], "completed": row[2]}

@app.patch("/todos/{todo_id}", status_code=200)
def update_todo(todo_id: int, todo: TodoUpdate, conn=Depends(get_conn)):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE todos SET completed = %s WHERE id = %s RETURNING id, title, completed",
        (todo.completed, todo_id)
    )
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    return {"id": str(row[0]), "title": row[1], "completed": row[2]}

@app.delete("/todos/{todo_id}", status_code=200)
def delete_todo(todo_id: int, conn=Depends(get_conn)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s RETURNING id", (todo_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    return {"message": "Todo deleted successfully"}

