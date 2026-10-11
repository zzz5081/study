from fastapi import FastAPI,Depends,HTTPException
from models import LoginIn,ChatIn,ChatOut,UsageOut
from auth import get_current_user,USERS,TOKENS
import secrets

app = FastAPI()
CALLS = []
def fake_llm(prompt: str) ->dict:
    return {
        "reply":f"(模拟回复) 你说的是: {prompt}",
        "prompt_tokens": len(prompt),
        "completion_tokens": 20
    }
@app.get('/health')
def health():
    return {'status': 'OK'}
@app.post('/auth/login')
def login(data: LoginIn):
    if data.username not in USERS:
        raise HTTPException(401,"用户不存在")
    user = USERS.get(data.username)
    if user['hashed_password'] != data.password:
        raise HTTPException(401,"密码错误")
    token = secrets.token_hex(8)
    TOKENS[token] = data.username
    return {"token":token}

@app.post('/v1/chat',
          responses={401: {'description': 'token 无效'}},
          response_model=ChatOut
          )
def chat(data: ChatIn,user: dict = Depends(get_current_user)):
         # responses = {401: {'description': 'token 无效'}},
         # response_model = ChatOut): 一开始写错了，写到方法里面了
    c = fake_llm(data.prompt)
    cost = (c['prompt_tokens'] + c['completion_tokens']) * 0.0001
    CALLS.append({
        'username': user['username'],
        'prompt_tokens': c['prompt_tokens'],
        'completion_tokens': c['completion_tokens'],
        'cost': cost
    })
    return {
        'reply': c['reply'],
        'prompt_tokens': c['prompt_tokens'],
        'completion_tokens': c['completion_tokens'],
        'cost': cost
    }

@app.get('/v1/usage',
         response_model= UsageOut,
         responses={401: {"description": '无记录'}})
def usage(user: str = Depends(get_current_user)):
    s = [x for x in CALLS if x['username'] == user['username']]
    call_count = len(s)
    total_tokens = sum([x['prompt_tokens'] + x['completion_tokens'] for x in s])
    total_cost = sum([x['cost'] for x in s])
    return {
        'username': user['username'],
        'call_count': call_count,
        'total_tokens': total_tokens,
        'total_cost': total_cost
    }