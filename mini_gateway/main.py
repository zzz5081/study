from fastapi import FastAPI,Depends,HTTPException
import secrets
from auth import USERS,TOKENS,get_current_user
from models import LoginIn,ChatOut,ChatIn,UsageOut

app = FastAPI()

CALLS = []

def fake_llm(prompt):
    return {'reply': f'(模拟回复) 你说的是: {prompt}','prompt_tokens': len(prompt),'completion_tokens': 20}
@app.get('/health')
def health():
    return {'status': "OK"}

@app.post('/auth/login')
def user_login(data: LoginIn):
    user = USERS.get(data.username)
    if not user:
        raise HTTPException(401,"用户不存在")
    if user['password'] != data.password:
        raise HTTPException(401,'密码错误')
    token = secrets.token_hex(8)
    TOKENS[token] = data.username
    return {"token": token}

@app.post('/v1/chat',
          response_model=ChatOut,
          responses={401: {"description":"token无效"}})
def chat(data: ChatIn,user = Depends(get_current_user)):
    c = fake_llm(data.prompt)
    cost =(c['prompt_tokens']+c['completion_tokens']) * 0.0001
    CALLS.append({
        'username': user['username'],
        'prompt_tokens': c['prompt_tokens'],
        'completion_tokens':c['completion_tokens'],
        'cost': cost,
    })
    return{
        'reply': c['reply'],
        'prompt_tokens': c['prompt_tokens'],
        'completion_tokens': c['completion_tokens'],
        'cost': cost,
    }

@app.get('/v1/usage',
         response_model=UsageOut,
         responses={401: {"description": "token 无效"}})
def usage(user = Depends(get_current_user)):
    mine = [ x for x in CALLS if x['username'] == user['username']]
    call_count = len(mine)
    total_tokens = sum(x['prompt_tokens'] + x['completion_tokens'] for x in mine)
    total_cost = sum(x['cost'] for x in mine)
    return {
        'username': user['username'],
        'call_count': call_count,
        'total_tokens': total_tokens,
        'total_cost': total_cost
    }