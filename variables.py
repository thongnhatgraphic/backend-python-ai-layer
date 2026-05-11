name = "john"
age = 20
price = 10.5
is_student = True



# # 1.1

# a = { 
#         "filter": { 
#             "status": "done" 
#         } 
#     }

# b = { 
#         "filter": { "priority": "high" } 
#     }

# print("a", { **a })
# print("b", { **b })

# merge_dict = {**a, **b}
# print("merge_dict", merge_dict)

# # 1.2
# default = {"status": "pending"}
# data = {"name": "Task A"}

# new_dict = {**default, **data}
# print("new_dict", new_dict)

# # 1.3 filter dict

# data_filter = {
#     "id": 1,
#     "name": "A",
#     "password": "123"
# }

# new_data_filter = data_filter.copy()
# new_data_filter.pop("password")

# print("data_filter", data_filter)
# print("new_data_filter", new_data_filter)

# # 🧠 PHẦN 2 — Class & Object
# class Task:
#     def __init__(self, id, name, status):
#         self.id = id
#         self.name = name
#         self.status = status
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "status": self.status
#         }
#     def update(self, status: str):
#         self.status = status
#         return {
#             "id": self.id,
#             "name": self.name,
#             "status": self.status
#         }
#     @classmethod
#     def from_dict(self, id, name, status):
#         self.id = id
#         self.name = name
#         self.status = status
#         return {
#             "id": id,
#             "name": name,
#             "status": status
#             }
# # 2.2
# task = Task(1, "A", "pending")

# task.update("done")

# # 🔥 Bài 2.3 — Init từ dict
# dict_class_method = {
#     "id": 1,
#     "name": "B",
#     "status": "pending"
# }
# task_init_from_dict = Task.from_dict(**dict_class_method)

# print('task_init_from_dict', task_init_from_dict)

# # 🧠 PHẦN 3 — List comprehension
# tasks = [
#     {"name": "A"},
#     {"name": "B"}
# ]

# tasks_value= [ task["name"] for task in tasks]
# print("tasks_value", tasks_value)

# # 🔥 Bài 3.2 — Filter
# tasks = [
#     {"name": "A", "status": "done"},
#     {"name": "B", "status": "pending"}
# ]

# tasks_done = [ task for task in tasks if task["status"] == "done"] 

# print("tasks_done", tasks_done)

# # 🔥 Bài 3.3 — SQL-like condition
# fields = ["name", "description"]

# new_fields = [ f"{field} ILIKE :search" for field in fields ]

# query = " AND ".join(new_fields)
# print("query", query)

a = {"filter": {"status": "done"}}
b = {"filter": {"priority": "high"}}
def deep_merge(a, b):
    result = a.copy()
    print('result', result)
    
    for key, value in b.items():
        if key in result and isinstance(result[key], dict):

            print('result[key]', result[key])
            print('result[key]', value)
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    
    return result
deep_merge(a, b)
# print(
#     deep_merge(a, b)
#     )
