# 1
listArray = list(range(1, 6))

for i in listArray:
    if i > 3:
        print("Greater than 3")
    else:
        print("Less than 3")

# 2
dictUser = {
    "name": "Nhat",
    "age": 32,
    "city": "Hue"
}

for key in dictUser:
    print(key, dictUser[key])

# 3
data = {
    "users": [
        {"name": "A", "age": 20},
        {"name": "B", "age": 17},
        {"name": "C", "age": 25}
    ]
}

for user in data["users"]: 
    if user["age"] >= 18:
        print(f"{user['name']} is an adult")
    else:
        print(f"{user['name']} is an child")

