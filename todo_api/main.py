from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.todos import router as todo_router

app = FastAPI(title="Todo API")

app.include_router(auth_router)
app.include_router(todo_router)

@app.get("/health")
def health():
    return {'status':'ok'}