import requests

url = "https://jsonplaceholder.typicode.com/users"


def fetch_users():
    try:
        response = requests.get(url)

        if response.status_code != 200:
            return []
        
        return response.json()
    except Exception as e:
        print("Error:", e)
        return []
    
def get_users_name(users):
    try:
        return [user["name"] for user in users]
    except Exception as e:
        print("Error:", e)
        return []
    
users = fetch_users()
print(get_users_name(users))

def get_users_by_city(users, city):
    try:
        return [user for user in users if user["address"]["city"] == city]
    except Exception as e:
        print("Error:", e)
        return []
    
print(get_users_by_city(users, "Gwenborough"))

url_post = "https://jsonplaceholder.typicode.com/posts"

payload = {
    "title": "Hello",
    "body": "Test API",
    "userId": 1
}

def create_post(payload):
    try:
        response = requests.post(url_post, json=payload)
        print(response.json())
        return response.json()
    except Exception as e:
        print("Error:", e)
        return []
# create_post(payload)
