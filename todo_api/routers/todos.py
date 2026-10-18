from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from db import get_db,Todo,User
from deps import get_current_user
from schemas import TodoIn,TodoOut,TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("",response_model=TodoOut,status_code=201)
def create_todo(body: TodoIn,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    todo = Todo(title=body.title,owner_id=current_user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@router.get("",response_model=list[TodoOut])
def list_todo(db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    return db.scalars(
        select(Todo).where(Todo.owner_id == current_user.id).order_by(Todo.id)
    ).all()

@router.patch("/{todo_id}",response_model=TodoOut)
def update_todo(todo_id: int,body: TodoUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    todo = db.get(Todo,todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(404,"todo 不存在")
    data = body.model_dump(exclude_unset=True)
    for k,v in data.items():
        setattr(todo,k,v)
    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/{todo_id}",status_code=204)
def delete_todo(todo_id: int,db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    todo = db.get(Todo,todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(404,"todo 不存在")
    db.delete(todo)
    db.commit()
    return None
    