import json
import asyncio

from fastapi import HTTPException, encoders
from app.models.task_model import Task
from datetime import datetime, timezone
from app.repositories.task_repository import TaskRepository
from uuid import UUID
from redis import Redis

class TaskService:
    def __init__(self, repository: TaskRepository, redis: Redis):
        self.repository = repository
        self.redis = redis

    def clear_task_cached(self, user_id: UUID):
        cached = [
            f"tasks:{user_id}:*",
            f"tasks_scale:{user_id}:*"
        ]

        for partern in cached:
            list_keys = list(self.redis.scan_iter(match=partern))
            self.redis.delete(*list_keys)

    @staticmethod
    def serialize_cursor(cursor_created_at):
        return cursor_created_at.isoformat() if cursor_created_at else "none"

    def create_task(self, name, progress, user_id):

        task = Task(name=name, progress = progress, status="pending")
        task.user_id = user_id
        
        print("\n task \n", task)

        result = self.repository.create_raw(task)

        if result is None:
            raise HTTPException(status_code=500, detail="Failed to create task")

        self.clear_task_cached(user_id)

        return result

    def get_tasks(self,
                  user_id: UUID, 
                  page, 
                  limit, 
                  status, 
                  priority, 
                  progress,
                  search, 
                  sort_by, 
                  order):

        search_key = search or "none"
        status_key = status or "all"
        priority_key = priority or "all"

        cache_key = f"tasks:{user_id}:{page}:{limit}:{status_key}:{priority_key}:{progress}:{search_key}:{sort_by}:{order}"
        
        print("\n cache key \n", cache_key)

        cached = self.redis.get(cache_key)
        if cached:
            print("Cache hit---", cached)
            return json.loads(cached)
        
        print("Hit DB")

        
        result = self.repository.get_tasks_raw(user_id, 
                                             page, 
                                             limit, 
                                             status, 
                                             priority, 
                                             progress,
                                             search, 
                                             sort_by, 
                                             order)
        
        self.redis.set(
            cache_key,
            json.dumps(encoders.jsonable_encoder(result)),
            ex=300,
            nx=True
        )

        return result
        # return self.repository.get_all(user_id,
        #                                page, 
        #                                limit, 
        #                                status, 
        #                                priority, 
        #                                search, 
        #                                sort_by, 
        #                                order)


    async def get_tasks_scale(self, 
                        cursor_created_at, 
                        cursor_id,
                        limit, 
                        status, 
                        priority, 
                        search, 
                        user_id: str):
        
        if limit < 10 or limit > 100:
            raise HTTPException(status_code=400, detail="Limit must be between 10 and 100")
        
        search_key = search or "none"
        status_key = status or "all"
        priority_key = priority or "all"
        cursor_created_at_key = self.serialize_cursor(cursor_created_at)
        cursor_id_key = cursor_id or "none"

        print("\n cursor_created_at_key \n", cursor_created_at_key)
        cache_key = f"tasks_scale:{user_id}:{cursor_created_at}:{cursor_id_key}:{limit}:{status_key}:{priority_key}:{search_key}"

        lock_key = f"tasks_scale_lock:{cache_key}"

        cached = self.redis.get(cache_key)
        if cached:
            return json.loads(cached)
        
        is_locked = self.redis.set(lock_key, "1", ex=5, nx=True)

        if is_locked:
            try:
                result = self.repository.get_tasks_scale_raw(
                cursor_created_at,
                cursor_id,
                limit,
                status,
                priority,
                search,
                user_id
            )
                
                self.redis.set(
                    cache_key, 
                    json.dumps(encoders.jsonable_encoder(result)),
                    ex=300
                )

                return result

            finally:
                print("final run here")
                self.redis.delete(lock_key)

        else:
            print("Cache miss")
            await asyncio.sleep(0.05)

            cached = self.redis.get(cache_key)
            if cached:
                print("Cache hit---", cached)
                return json.loads(cached)
            
            return self.repository.get_tasks_scale_raw(
                cursor_created_at,
                cursor_id,
                limit,
                status,
                priority,
                search,
                user_id
            )

    def delete_task(self, task_id, user_id: UUID):
        print('\n user_id \n\n', user_id)
        task = self.repository.get_by_id_and_user_id_raw(task_id, user_id)
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        cached = self.redis.scan_iter(match=f"tasks:{user_id}:*") or self.redis.scan_iter(match=f"tasks_scale:{user_id}:*")
        
        keys = list(self.redis.scan_iter(match=f"{cached}:*"))
        self.redis.delete(*keys)

        return self.repository.delete_raw(task_id, user_id)

    def update_task(self, task_id, name, progress, user_id):
        task = self.repository.get_by_id_and_user_id_raw(task_id, user_id)
        print('task', task)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # task.name = name
        # task.progress = progress
        # task.updated_at = datetime.now(timezone.utc)
        updated_at = datetime.now(timezone.utc)

        task_updated = self.repository.update_raw(task, name, progress, updated_at, user_id)

        if task_updated is None:
            raise HTTPException(status_code=500, detail="Failed to update task")

        self.clear_task_cached(user_id)

        return task_updated

    def get_task(self, task_id, user_id: UUID):
        task = self.repository.get_by_id_and_user_id_raw(task_id, user_id)

        print(task)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return task
        
    def complete_task(self, task_id, user_id: UUID):
        task = self.repository.get_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        task.status = "completed"
        task.progress = 100
        task.updated_at = datetime.now(timezone.utc)

        task_updated = self.repository.update(task)

        if task_updated is None:
            raise HTTPException(status_code=500, detail="Failed to update task")
        
        self.clear_task_cached(user_id)

        return task_updated
    
    def complete_multiple_tasks(self, task_ids: list[int], user_id: UUID):
        print('task_ids', task_ids)
        return self.repository.complete_multiple_tasks(task_ids, user_id)