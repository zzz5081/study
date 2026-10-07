from fastapi import FastAPI,HTTPException,Depends,Header

app = FastAPI()
USERS={}

def get_current_user(token: str = Header(default="")):
    if token is None:
        raise HTTPException(401,"token 不存在")
    user = USERS.get(token)
    if user is None:
        raise HTTPException(401,"token 失效")
    return user

@app.get('/user')
def user(user = Depends(get_current_user)):
    return user['name']

@app.get('/user_order')
def user_order(user = Depends(get_current_user)):
    return {"name": user["name"],"订单": ["订单1","订单2"]}