# 实验：注册 / 登录的完整逻辑（bcrypt + JWT 组装）—— 2026-10-14（W6 Day 3）
#
# 关键点：
#   1. 注册：密码 --bcrypt.hashpw--> 存哈希（库里【没有明文】）
#   2. 登录：bcrypt.checkpw 验密码 -> 通过则 jwt.encode 发 token
#   3. ⭐ JWT 的 payload 是【明文】，所以【绝不放密码】
#   4. exp 必须用 datetime.datetime.now(datetime.timezone.utc)
#      （用 naive 的 datetime.now() 会被当成 UTC，中国时区下差 8 小时）
#   5. 这是【纯函数】版，不涉及 Web 框架 —— 周六用 FastAPI 包一层路由就是完整接口
#
# 我踩的坑：
#   · _next_id 忘了自增 -> 所有用户 id 都是 1
#   · 修了自增后 id 从 2 开始 -> ★「什么时候 +1」和「初始值」必须【配套】：
#         先加再用 -> 初始值 = 起始编号 - 1（想从 1 开始就写 0）
#         先用再加 -> 初始值 = 起始编号
#   · 测试过期 token 的办法：不改 login，手工造一个 exp 是【过去】的 token
#     （测试不该为了测试去改被测代码）
#
import bcrypt,jwt,secrets,datetime
# from jwt_手工实现_实验 import make_jwt
SECRET_KEY = secrets.token_hex(32)
FAKE_DB = {}
_next_id = 0

def register(username: str,password: str) -> int:
    user = FAKE_DB.get(username)
    if user:
        raise ValueError("用户名已存在")
    h = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    global _next_id
    _next_id += 1
    FAKE_DB[username] = {'id': _next_id,'pwd_hash': h}
    return _next_id

def login(username: str,password: str) ->str | None:
    user = FAKE_DB.get(username)
    if not user:
        return None
    if bcrypt.checkpw(password.encode(),user['pwd_hash']):
        payload = {
            "user_id": user['id'],
            "username": username,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours = 2),
        }
        user_jwt = jwt.encode(payload,SECRET_KEY,algorithm= 'HS256')
        return user_jwt

uid = register("zhong","123456")
print("user_id=",uid)
print("FAKE_DB",FAKE_DB)
token = login('zhong','123456')
print(token)
print(login('zhong','wrong'))
print(login('nobody','123456'))
print(jwt.decode(token,SECRET_KEY,algorithms=["HS256"]))
register('zhong1','123456')
print(FAKE_DB)

past = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=10)
expired = jwt.encode({'user_id': 1,'exp': past},SECRET_KEY,algorithm="HS256")

try:
    jwt.decode(expired,SECRET_KEY,algorithms=['HS256'])
    print("没报错?")
except jwt.ExpiredSignatureError as e:
    print((f"正确 {type(e).__name__}: {e}"))
