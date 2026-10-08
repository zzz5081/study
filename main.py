from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    age: int
    email: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}
@app.get("/about")
def about():
    return {"我的名字是":"钟","goal":"mi"}
@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id, "类型": type(user_id).__name__}
@app.get("/users")
def list_users(skip: int = 5,limit: int = 10):
    return {"skip": skip,"limit": limit}
@app.post("/users")
def create_user(user: UserCreate):
    return {"收到":user,"名字": user.name}

FAKE_DB = {1: {"id":1, "name":"张三"}, 2: {"id": 2, "name":"李四"}}

@app.get("/items/{item_id}",
         responses={
             404: {"description" : "item 不存在"},
         },
)
def get_item(item_id: int):
    if item_id not in FAKE_DB:
        raise HTTPException(status_code=404, detail="这个 item 不存在")
    return  FAKE_DB[item_id]

class UserOut(BaseModel):
    id: int
    name: str

@app.get("/safe-users/{user_id}",
         responses={
             404: {"description" : "用户不存在"}
         },
response_model=UserOut)
def get_user_safe(user_id: int):
    row = FAKE_DB.get(user_id)
    if row is None:
        raise HTTPException(status_code=404,detail="用户不存在")
    row = {**row,"password":"超级哈希机密"}
    return row