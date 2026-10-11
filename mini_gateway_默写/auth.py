from fastapi import HTTPException,Header

USERS = {"zhong": {"username": "zhong","hashed_password": "假哈希","api_key":"sk-绝密"}}
TOKENS = {}

def get_current_user(token: str = Header(default="")):
    if not token:
        raise HTTPException(401,"token 不存在")
    user = TOKENS.get(token)
    if not user:
        raise HTTPException(401,"token 失效")
    username = user
    return USERS[username]