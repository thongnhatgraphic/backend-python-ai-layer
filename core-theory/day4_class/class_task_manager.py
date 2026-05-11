import json
import time
import asyncio


class TaskManager: 
    def __init__(self):
        self.tasks = {}
        self.id = 0

    
    def add_task(self, name): 
        self.id += 1
        self.tasks[self.id] = {"id": self.id, "name": name, "status": "pending"}


    def complete_task(self, id):
        if id in self.tasks:
            self.tasks[id]["status"] = "completed"
            return True
        else:
            print("Task not found")
            return False
        
    def delete_task(self, id):
        if id in self.tasks:
            self.tasks.pop(id)
            return True
        return False

    def update_task(self, id, new_name):
        if id in self.tasks:
            self.tasks[id]["name"] = new_name
            return True
        return False

    async def async_add_task(self, name):
        await asyncio.sleep(1)
        self.add_task(name)
        print(f"Added task {name}")
        return name

    def list_tasks(self):
        return list(self.tasks.values())
    

my_task = TaskManager()

# my_task.add_task("Learning python and AI Engineering")

# my_task.add_task("Learning python class")

# my_task.add_task("practice with class")

# my_task.add_task("practice with async / await")

# my_task.add_task("Learn FastApi")

# my_task.complete_task(2)



# async def batch_tasks():
#     await asyncio.gather(
#         my_task.async_add_task("A"),
#         my_task.async_add_task("B"),
#         my_task.async_add_task("C"),
#     )
# print(my_task.list_tasks())
# asyncio.run(batch_tasks())
# print(my_task.list_tasks())
# # my_task.delete_task(3)
# # my_task.update_task(1, "Learning python and AI Engineering Hardly")


# # Bài tập 2:

# def divide(a,b):
#     if b == 0:
#         return "Cannot divide by zero"
#     return a / b
    
# divide(10,0)


# # Bài tập 3: File Handling

# with open("core/day4_class/data.json", "w") as f:
#     json.dump(my_task.list_tasks(), f, indent=2)

# with open("core/day4_class/data.json", "r") as f:
#     data = json.load(f)
#     print(data)


# # Async / Await:

# async def fetch_data(name, delay):
#     await asyncio.sleep(delay)
#     return f"Done {name}"

# async def save_task():
#     await asyncio.sleep(2)
#     print("Saved")


# async def done_task(task_name):
#     print(f"Start {task_name}")
#     await asyncio.sleep(1)
#     print(f"Done adding Task {task_name}")
#     return f"Done adding Task {task_name}"

# async def main():
#     return await asyncio.gather(done_task("A"), done_task("B"), done_task("C"))



# result = asyncio.run(main())

# print(result)


