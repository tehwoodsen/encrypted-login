from cryptography.fernet import Fernet

def load_key():
    try:
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

KEY = load_key()
cipher = Fernet(KEY)
import bcrypt
import json

# this is the user database
USER_DB = "users.json"

# this will load the users from the JSON file
def load_users():
    try:
        with open(USER_DB, "rb") as f:
            encrypted = f.read()
            decrypted = cipher.decrypt(encrypted)
            return json.loads(decrypted.decode())
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"[Error] Could not load users: {e}")
        return {}

# this saves the user dictionary to the file
def save_users(users):
    data = json.dumps(users).encode()
    encrypted = cipher.encrypt(data)
    with open(USER_DB, "wb") as f:
        f.write(encrypted)

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