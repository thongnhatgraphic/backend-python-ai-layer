from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session 
from uuid import UUID

from app.database import get_session
from app.response_schema.task_schema import TaskResponse
from app.response_schema.delete_response import DeleteResponse
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.dependencies.auth_dependency import get_current_user

router = APIRouter()


def get_task_service(session: Session = Depends(get_session)):
    repo = TaskRepository(session)
    return TaskService(repo)

class TaskRequest(BaseModel):
    name: str
    progress: int

@router.get("/tasks", response_model= list[TaskResponse])
async def get_tasks(
    user_id: str = Depends(get_current_user),
    taskService: TaskService = Depends(get_task_service)
    ):
    return taskService.get_tasks(user_id)

@router.get("/task/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    taskService: TaskService = Depends(get_task_service)):
    return taskService.get_task(task_id, user_id)

@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task : TaskRequest, 
    user_id: UUID = Depends(get_current_user),
    taskService: TaskService = Depends(get_task_service)):
    return taskService.create_task(task.name, user_id)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
        task_id: int,
        task: TaskRequest, 
        user_id: UUID = Depends(get_current_user),
        taskService: TaskService = Depends(get_task_service)):
    return taskService.update_task(task_id, task.name, task.progress, user_id)


@router.delete("/tasks/{task_id}", response_model=DeleteResponse)
async def delete_task(
    task_id: int,
    user_id: UUID = Depends(get_current_user),
    taskService: TaskService = Depends(get_task_service)):
    return taskService.delete_task(task_id, user_id)
    

@router.put('/tasks/{task_id}/complete', response_model=TaskResponse)
async def complete_task(
    task_id: int, 
    user_id: UUID = Depends(get_current_user),
    taskService: TaskService = Depends(get_task_service)):
    return taskService.complete_task(task_id, user_id)