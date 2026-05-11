data = {
    "users": [
        {"name": "A", "age": 20},
        {"name": "B", "age": 17},
        {"name": "C", "age": 25}
    ]
}

# output
# {
#   "adult": ["A", "C"],
#   "child": ["B"]
# }

adult = [ user["name"] for user in data["users"] if user["age"] >= 18 ]
child = [ user["name"] for user in data["users"] if user["age"] < 18 ]

response = {
    "adult": adult,
    "child": child
}

print(response)

list_age_users = [ user["age"] for user in data["users"]]
if list_age_users:
    average_ages = sum(list_age_users) / len(list_age_users)
else:
    average_ages = 0

print(average_ages)
