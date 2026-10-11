from fastapi import Header,HTTPException

USERS = {"zhong": {"username": "zhong","password": "123456"}}
TOKENS = {}
def get_current_user(token: str = Header(default="")):
    if not token:
        raise HTTPException(401,'token 不存在')
    if token not in TOKENS:
        raise HTTPException(401,"token 失效")
    username = TOKENS[token]
    return USERS[username]