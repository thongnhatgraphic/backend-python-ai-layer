from fastapi import HTTPException
from app.models.task_model import Task
from datetime import datetime, timezone
from app.repositories.task_repository import TaskRepository
from uuid import UUID


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, name, user_id):
        task = Task(name=name, status="pending")
        task.user_id = user_id
        
        print("\n task \n", task)

        self.repository.create(task)
        return task

    def get_tasks(self, user_id: UUID):
        return self.repository.get_all(user_id)

    def delete_task(self, task_id, user_id: UUID):
        print('\n user_id \n\n', user_id)
        task = self.repository.get_by_id_and_user_id(task_id, user_id)
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # self.repository.delete(task)
        return {"id": task_id}

    def update_task(self, task_id, name, progress, user_id):
        task = self.repository.get_by_id_and_user_id(task_id, user_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.name = name
        task.progress = progress
        task.updated_at = datetime.now(timezone.utc)

        return self.repository.update(task)

    def get_task(self, task_id, user_id: UUID):
        task = self.repository.get_by_id_and_user_id(task_id, user_id)

        print(task)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return task
        
    def complete_task(self, task_id):
        task = self.repository.get_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.status = "completed"
        task.progress = 100
        task.updated_at = datetime.now(timezone.utc)

        return self.repository.update(task)