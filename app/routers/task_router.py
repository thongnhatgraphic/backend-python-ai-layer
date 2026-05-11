from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlmodel import Session 
from uuid import UUID
from datetime import datetime
import redis

from app.dependencies.redis_dependency import get_redis_client
from app.database import get_session
from app.response_schema.task_schema import TaskResponse, TaskPaginationResponse
from app.response_schema.delete_response import DeleteResponse
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.dependencies.auth_dependency import get_current_user

router = APIRouter()

def get_task_service (
        session: Session = Depends(get_session),
        cache: redis.Redis = Depends(get_redis_client)                 
    ):
    repo = TaskRepository(session)
    return TaskService(repo, cache)

class TaskRequest(BaseModel):
    name: str
    progress: int

@router.get("/tasks", response_model= TaskPaginationResponse)
async def get_tasks(
    page: int = 1,
    limit: int = 10,
    status: str | None = None,
    priority: int | None = None,
    progress: int | None = None,
    search: str | None = None,
    sort_by: str = 'created_at',
    order: str = 'desc',
    user_id: str = Depends(get_current_user),
    taskService: TaskService = Depends(get_task_service)
    ):
    print()
    return taskService.get_tasks(user_id, 
                                 page, 
                                 limit, 
                                 status, 
                                 priority, 
                                 progress,
                                 search, 
                                 sort_by, 
                                 order)

# , response_model= TaskPaginationResponse
@router.get("/tasks-scale")
async def get_tasks_scale(
        cursor_created_at: datetime | None = None,
        cursor_id: int | None = None,
        limit: int = 10,
        status: str | None = None,
        priority: int | None = None,
        search: str | None = None,
        user_id: UUID = Depends(get_current_user),
        taskService: TaskService = Depends(get_task_service)
    ):
    return taskService.get_tasks_scale( cursor_created_at,
                                        cursor_id,
                                        limit,
                                        status,
                                        priority,
                                        search,
                                        user_id
                                       )


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
    return taskService.create_task(task.name, task.progress, user_id)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
        task_id: int,
        task: TaskRequest, 
        user_id: UUID = Depends(get_current_user),
        taskService: TaskService = Depends(get_task_service)):
    return taskService.update_task(task_id, task.name, task.progress, user_id)


@router.delete("/tasks/{task_id}", response_model=TaskResponse)
async def delete_task(
    task_id: int,
    user_id: UUID = Depends(get_current_user),
    taskService: TaskService = Depends(get_task_service)):
    return taskService.delete_task(task_id, user_id)
    
@router.put('/tasks/multiple/complete', response_model=list[TaskResponse])
async def complete_multiple_tasks(
    task_ids: list[int], 
    user_id: UUID = Depends(get_current_user),
    taskService: TaskService = Depends(get_task_service)):
    print("hello words")
    return taskService.complete_multiple_tasks(task_ids, user_id)

@router.put('/tasks/{task_id}/complete', response_model=TaskResponse)
async def complete_task(
    task_id: int, 
    user_id: UUID = Depends(get_current_user),
    taskService: TaskService = Depends(get_task_service)):
    return taskService.complete_task(task_id, user_id)
