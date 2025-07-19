import requests
import random
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get port from .env (fallback to 8000 if not set)
PORT = os.getenv("PORT", 8000)
BASE_URL = f"http://localhost:{PORT}/api/"

# Dummy user data
dummy_users = [
    {
        "name": "Alice Sharma",
        "email": "alice.sharma@example.com",
        "password": "AlicePass123",
        "dob": "2001-05-12",
        "semester_id": 1
    },
    {
        "name": "Bob Mehta",
        "email": "bob.mehta@example.com",
        "password": "BobSecret456",
        "dob": "2002-08-25",
        "semester_id": 2
    },
    {
        "name": "Charlie Dutta",
        "email": "charlie.dutta@example.com",
        "password": "Charlie789!",
        "dob": "2003-11-15",
        "semester_id": 3
    }
]

def register_user(user):
    try:
        response = requests.post(f"{BASE_URL+'auth/register'}", json=user)
        if response.status_code == 200:
            print(f"Registered: {user['email']}")
        elif response.status_code == 409:
            print(f"Already exists: {user['email']}")
        else:
            print(f"Failed for {user['email']}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def load_dummy_users():
    for user in dummy_users:
        register_user(user)

if __name__ == "__main__":
    load_dummy_users()