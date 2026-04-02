from datetime import datetime, timezone, timedelta
from sqlmodel import SQLModel, Field
from uuid import UUID

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = ''
    status: str = 'pending'
    description: str = 'Study hard, work hard, learning is very important!!!'
    progress: int = 0  # 0 -> 100
    priority: int = 0
    deadline: datetime | None = None
    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    # user_id: UUID = Field(foreign_key="usermodel.id")

# import asyncio

# class TaskManager: 
#     def __init__(self):
#         self.tasks = {}
#         self.id = 0

    
#     def add_task(self, name): 
#         self.id += 1
#         self.tasks[self.id] = {"id": self.id, "name": name, "status": "pending"}


#     def complete_task(self, id):
#         if id in self.tasks:
#             self.tasks[id]["status"] = "completed"
#             return True
#         else:
#             print("Task not found")
#             return False
        
#     def delete_task(self, id):
#         if id in self.tasks:
#             self.tasks.pop(id)
#             return True
#         return False

#     def update_task(self, id, new_name):
#         if id in self.tasks:
#             self.tasks[id]["name"] = new_name
#             return True
#         return False

#     async def async_add_task(self, name):
#         await asyncio.sleep(1)
#         self.add_task(name)
#         print(f"Added task {name}")
#         return name

#     def list_tasks(self):
#         return list(self.tasks.values())
    
