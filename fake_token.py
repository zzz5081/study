header = {"alg": "none", "typ": "JWT"}
payload = {"user_id": 1,"username": "zhong","exp": 1766000000}

import base64,json,hashlib,hmac
h = base64.urlsafe_b64encode(
    json.dumps(header,separators=(',',':'),ensure_ascii=False).encode('utf-8')
).rstrip(b'=').decode('utf-8')
p = base64.urlsafe_b64encode(
    json.dumps(payload,separators=(',',':'),ensure_ascii=False).encode('utf-8')
).rstrip(b'=').decode('utf-8')
fake_token = f"{h}.{p}."
print(fake_token)

from todo_api import security
try:
    security.decode_token(fake_token)
    print("! 通过了 --- 危险")
except Exception as e:
    print(type(e).__name__,":",e)

import jwt
try:
    jwt.decode(fake_token,security.SECRET_KEY,algorithms=["none"],
               options={"verify_signature": False})
    print("! 放宽后通过了 -- 说明这行代码是唯一的门")
except Exception as e:
    print(type(e).__name__,":",e)