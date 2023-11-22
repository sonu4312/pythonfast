from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

# Database setup
conn = sqlite3.connect('todo.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tasks 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              task_name TEXT,
              created_on DATE,
              status TEXT)''')
conn.commit()
conn.close()


# Function to add a task
def create_task(task_name):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task_name, created_on, status) VALUES (?, datetime('now'), ?)",
              (task_name, 'Pending'))
    conn.commit()
    conn.close()


# Function to delete a task
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


# Function to show all tasks
def show_tasks():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task_name, created_on, status FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks


# Function to mark a task as done
def mark_task_done(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET status='Done' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


@app.post("/tasks/create/{task_name}")
def create_new_task(task_name: str):
    create_task(task_name)
    return {"message": f"Task '{task_name}' created successfully"}


@app.delete("/tasks/delete/{task_id}")
def delete_existing_task(task_id: int):
    delete_task(task_id)
    return {"message": f"Task with ID {task_id} deleted successfully"}


@app.get("/tasks/show")
def show_all_tasks():
    tasks = show_tasks()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return {"tasks": tasks}


@app.put("/tasks/done/{task_id}")
def mark_task_as_done(task_id: int):
    mark_task_done(task_id)
    return {"message": f"Task with ID {task_id} marked as done"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
