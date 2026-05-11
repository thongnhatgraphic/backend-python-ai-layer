data = {
    "users": [
        {"name": "A", "age": 20},
        {"name": "B", "age": 17},
        {"name": "C", "age": 25},
        {"name": "D", "age": 15}
    ]
}

adult_user = [user for user in data["users"] if user["age"] >=18 ]


print(adult_user)

# transform data
transform_data_users = [ f"{user['name']} - {user['age']}" for user in data["users"] if user["age"] >= 18]

print(transform_data_users)

# oldest user
oldest_user = None

for user in data["users"]:
    if oldest_user is None or oldest_user["age"] < user["age"]:
        oldest_user = user

print(oldest_user)

response = {
    "data": {
        "coins": [
            {"name": "BTC", "price": 60000},
            {"name": "ETH", "price": 3000}
        ]
    }
}

for coin in response["data"]["coins"]:
    print(f"{coin["name"]}: {coin["price"]}")