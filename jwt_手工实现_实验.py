# 题型：手工实现 JWT（HS256）+ 与 pyjwt 互通验证  —— 2026-10-13
#
# 关键点：
#   1. JWT = base64url(header) + "." + base64url(payload) + "." + base64url(签名)
#   2. ⭐ payload 是【明文】—— base64 只是编码，不是加密，任何人都能解出来
#      → 所以 payload 里【绝不能】放敏感信息
#   3. 签名 = HMAC-SHA256(secret, "header.payload")；改一个字签名就对不上
#   4. ⭐ 解码 = 编码每一步【反着做】，而且顺序整体倒过来
#   5. secret 是唯一要保密的东西，必须 ≥32 字节随机（pyjwt 会警告太短）
#
# 我踩的坑：
#   · verify 里把"解码"写成"再编码一遍"（json.dumps 一个字符串）→ 应该 json.loads
#   · .rstrip(b"=") 是编码时的动作；解码要【补回】填充
#   · f"{bytes}" 会带出 b'' —— 要先 .decode()
#   · HMAC-SHA256(secret, input) 不是 Python —— ★ 第 2 次「把概念写成代码」
#     （第 1 次是 10/12 爬楼梯的 f(n) = f(n-1) + f(n-2)）
#
import base64

import hmac,hashlib,json

def make_jwt(payload: dict,secret: str) ->str:
    def enc(obj) -> str:
        """dict -> JSON bytes ->base64url(不带填充) -> str"""
        return base64.urlsafe_b64encode(
            json.dumps(obj,separators=(',',':')).encode()
        ).rstrip(b"=").decode()
    h = enc({'alg':"HS256","typ":"JWT"})
    p = enc(payload)
    signing_input = f"{h}.{p}"
    raw_sig = hmac.new(
        secret.encode(),
        signing_input.encode(),
        hashlib.sha256
    ).digest()
    sig = base64.urlsafe_b64encode(raw_sig).rstrip(b"=").decode()
    return f"{h}.{p}.{sig}"

t = make_jwt({"user_id": 1,"name": "zhong"},"mysecret")
print(t)

def verify_jwt(jwt,secret: str):
    parts = jwt.split('.')
    h = parts[0]
    p = parts[1]
    s = parts[2]
    signing_input = f"{h}.{p}"
    raw_sig = hmac.new(
        secret.encode(),
        signing_input.encode(),
        hashlib.sha256
    ).digest()
    sig = base64.urlsafe_b64encode(raw_sig).rstrip(b"=").decode()
    if sig == s:
        padded = p + "=" * (-len(p) % 4)
        json_bytes = base64.urlsafe_b64decode(padded)
        json_str = json_bytes.decode()
        return json.loads(json_str)
    else:
        return None

print(verify_jwt(t,'mysecret'))
print(verify_jwt(t, "wrong-secret"))
print(verify_jwt("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyXlkIjoxLCJuYW1lIjoiemhvbmcifQ.-Jm--60QuIzH6abW1EjvQ7CqXfeYB-tiIPUwfnJpEG8",'mysecret'))
print(make_jwt({"a":1}, "s"))
if __name__ == '__main__':

    # ★ 和 pyjwt 互通测试
    import jwt, secrets
    SECRET = secrets.token_hex(32)          # ★ 用够长的，避免警告

    mine = make_jwt({"user_id": 1, "name": "zhong"}, SECRET)
    assert jwt.decode(mine, SECRET, algorithms=["HS256"]) == {"user_id": 1, "name": "zhong"}
    assert verify_jwt(jwt.encode({"a": 1}, SECRET, algorithm="HS256"), SECRET) == {"a": 1}
    assert mine == jwt.encode({"user_id": 1, "name": "zhong"}, SECRET, algorithm="HS256")  # ★ 字节一致
    print("与 pyjwt 完全一致 ✅")