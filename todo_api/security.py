import os,bcrypt,jwt,datetime

SECRET_KEY = os.environ.get("APP_SECRET")
if not SECRET_KEY:
    raise RuntimeError("请先设置环境变量 APP_SECRET_KEY")

def hash_password(password: str) ->bytes:
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt())

def verify_password(password: str,hashed: bytes)-> bool:
    h = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    return h == hashed

def create_token(user_id: int, username: str, hours: int = 2) ->str:
    payload = {
        'user_id':user_id,
        'username':username,
        'hours':hours
    }
    return jwt.encode(payload,SECRET_KEY,algorithm='HS256')

def decode_token(token: str) -> dict:
    return jwt.decode(token,SECRET_KEY,algorithms='HS256')

# t = create_token(1,'张三',2)
# print(t)
# print(decode_token(t))
