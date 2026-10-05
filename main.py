from fastapi import FastAPI
from pydantic import BaseModel

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
def list_users(skip: int,limit: int = 10):
    return {"skip": skip,"limit": limit}
@app.post("/users")
def create_user(user: UserCreate):
    return {"收到":user,"名字": user.name}
