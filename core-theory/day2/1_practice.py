data = {
    "users": [
        {"name": "A", "age": 20},
        {"name": "B", "age": 17},
        {"name": "C", "age": 25}
    ]
}

def get_adult_users(users):
    result = []
    for user in users:
        if user["age"] >= 18:
            result.append(user)
    return result

def format_users(users):
    result = []
    for user in users:
        result.append(f"{user['name']} - {user['age']}")
    return result

def get_average_age(users):
    if len(users) == 0:
        return 0
    
    total_age = 0
    for user in users:
        total_age += user["age"]

    return total_age / len(users)

print(get_adult_users(data["users"]))
adult_users = get_adult_users(data["users"])

print(format_users(adult_users))
print(get_average_age(data["users"]))


response = {
    "data": {
        "coins": [
            {"name": "BTC", "price": 60000},
            {"name": "ETH", "price": 3000}
        ]
    }
}

def get_coin_prices(coins):
    try:
        coins = response["data"]["coins"]
        return [f"{coin['name']}: {coin['price']}" for coin in coins]
    except Exception as e:
        print("Error:", e)
        return []

print(get_coin_prices(response["data"]["coins"]))