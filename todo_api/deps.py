import jwt
from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from security import decode_token
from db import get_user

bear_scheme = HTTPBearer(auto_error=False)

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bear_scheme)):
    if creds is None:
        raise HTTPException(401, "未提供 token")

    try:
        payload = decode_token(creds.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "token 已过期")
    except jwt.InvalidSignatureError:
        raise HTTPException(401, "token 签名无效")
    except jwt.DecodeError:
        raise HTTPException(401, "token 格式错误")

    user = get_user(payload["username"])
    if not user:
        raise HTTPException(401, "token 对应的用户不存在")
    return user