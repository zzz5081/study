from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
@app.get("/about")
def about():
    return {"我的名字是":"钟","goal":"mi"}