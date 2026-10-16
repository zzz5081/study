from fastapi import APIRouter,HTTPException
from security import hash_password
from schemas import UserOut,RegisterIn
from db import get_user,create_user
router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",response_model=UserOut,status_code=201)
def register(body: RegisterIn):
    user = get_user(body.username)
    if user:
        raise HTTPException(409,"用户名重复")
    id = create_user(body.username,hash_password(body.password))
    return {'id':id,"username":body.username}

# □ POST /auth/register  新用户 ─────────────→ 201 {"id":1,"username":"zhong"}
# □ POST /auth/register  同一用户名再来一次 ──→ 409（★ 不能是 500）
# □ POST /auth/register  密码 "123" ─────────→ 422
# □ POST /auth/register  密码 80 个字符 ─────→ 422（★ 不能是 500）
# □ POST /auth/register  用户名 "ab" ────────→ 422
# □ 🔴 返回体里搜索不到 password / pwd_hash / $2b$
# □ 🔴 重启 uvicorn，再注册一个用户 → id 从 2 开始（说明内存被重置，正常）
# □ /docs 的 auth 分组里看到 /auth/register，标注 201