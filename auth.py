import bcrypt
import json

# this is the user database
USER_DB = "users.json"

# this will load the users from the JSON file
def load_users():
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# this saves the user dictionary to the file
def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# had to ask the llm to help with how to register a new user only if username doesn't already exist
def register_user(username, password):
    users = load_users()
    if username in users:
        return False  # Username already exists
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users[username] = hashed_pw.decode()  # Store as string
    save_users(users)
    return True

# standard return check if the provided credentials are valid
def authenticate_user(username, password):
    users = load_users()
    if username not in users:
        return False
    stored_hash = users[username].encode()  # Convert back to bytes
    return bcrypt.checkpw(password.encode(), stored_hash)