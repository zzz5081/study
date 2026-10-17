from fastapi import APIRouter,HTTPException,Depends
from security import hash_password,verify_password,create_token
from schemas import UserOut,RegisterIn,LoginIn,TokenOut
from db import get_user,create_user
from deps import get_current_user

router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",response_model=UserOut,status_code=201)
def register(body: RegisterIn):
    user = get_user(body.username)
    if user:
        raise HTTPException(409,"用户名重复")
    id = create_user(body.username,hash_password(body.password))
    return {'id':id,"username":body.username}

@router.post("/login",response_model=TokenOut)
def login(body: LoginIn):
    user = get_user(body.username)
    if not user:
        raise HTTPException(401,"用户名或密码错误")
    if not verify_password(body.password,user["pwd_hash"]):
        raise HTTPException(401,"用户名或密码错误")
    token = create_token(user["user_id"],body.username)
    return {"access_token": token, "token_type":"bearer"}

@router.get("/me",response_model=UserOut)
def me(current_user: dict = Depends(get_current_user)):
    return {'id': current_user["user_id"],"username": current_user["username"]}