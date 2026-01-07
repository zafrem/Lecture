from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users = {}  # {username: {"password": 해시된_비번}}

def get_user(username: str):
    return fake_users.get(username)

def create_user(username: str, password: str):
    hashed = pwd_context.hash(password)
    fake_users[username] = {"password": hashed}

def delete_user(username: str):
    fake_users.pop(username, None)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
