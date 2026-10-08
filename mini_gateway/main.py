from fastapi import FastAPI,Depends,HTTPException
import secrets
from auth import USERS,TOKENS,get_current_user
from models import LoginIn

app = FastAPI()

CALLS = []

@app.get('/health')
def health():
    return {'status': "OK"}

@app.post('/auth/login')
def user_login(data: LoginIn):
    user = USERS.get(data.username)
    if not user:
        raise HTTPException(401,"用户不存在")
    if user['password'] != data.password:
        raise HTTPException(401,'密码错误')
    token = secrets.token_hex(8)
    TOKENS[token] = data.username
    return {"token": token}
