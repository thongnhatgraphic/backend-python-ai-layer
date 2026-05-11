import asyncio

from fastapi import FastAPI
from fastapi import HTTPException

from pydantic import BaseModel
from core.day4_class.class_task_manager import TaskManager


app = FastAPI()
task_manager = TaskManager()

class TaskRequest(BaseModel):
    name: str

@app.get("/tasks")
def get_tasks():
    list_tasks = task_manager.list_tasks()

    return {
        "message": "List of tasks",
        "data": list_tasks
    }

@app.post("/tasks", status_code=201)
def add_task(task : TaskRequest):
    task_manager.add_task(task.name)
    return {
        "message": "Task added",
        "data": task_manager.list_tasks()[-1]
    }


@app.delete("/tasks/{task_id}")
def delete_task(task_id : int):
    is_deleted = task_manager.delete_task(task_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "message": "Task deleted",
        "data": { "id": task_id }
    }

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task : TaskRequest):
    is_updated = task_manager.update_task(task_id, task.name)

    if not is_updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "message": "Task updated",
        "data": task.model_dump()
    }
    
@app.post("/tasks/async", status_code=201)
async def add_task_async(task : TaskRequest):
    await asyncio.sleep(1)
    task_manager.add_task(task.name)

    return {
        "message": "Task added",
        "data": task.model_dump()
    }