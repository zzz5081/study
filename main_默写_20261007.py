from fastapi import FastAPI,HTTPException,Header,Depends
from fastapi.testclient import TestClient

app = FastAPI()

USERS = {
    "token-zhang": {"id":1, "name": "张三","role": "admin"},
    "token-li": {"id": 2,"name": "李四", "role": "user"}
}

def get_current_user(token: str = Header(default="")):
    if not token:
        raise HTTPException(401,"缺少 token")
    user = USERS.get(token)
    if user is None:
        raise HTTPException(401,"token 无效")
    return user

@app.get("/me")
def read_me(user=Depends(get_current_user)):
    return {"我是": user["name"]}

@app.get("/my-orders")
def my_orders(user=Depends(get_current_user)):
    return {"用户": user["name"],"订单": ["订单A","订单B"]}

if __name__ == "__main__":
    c = TestClient(app)

    r = c.get("/me", headers={"token": "token-li"})
    print("带对的token ->", r.status_code, r.json())

    r = c.get("/me")
    print("不带token   ->", r.status_code, r.json())

    r = c.get("/me", headers={"token": "wrong"})
    print("带错的token ->", r.status_code, r.json())

    r = c.get("/my-orders", headers={"token": "token-zhang"})
    print("张三的订单  ->", r.status_code, r.json())