from pydantic import BaseModel,Field

class LoginIn(BaseModel):
    username: str
    password: str

class ChatIn(BaseModel):
    prompt: str = Field(min_length=1,max_length=200)
class ChatOut(BaseModel):
    reply: str
    prompt_token: int
    completion_token: int
    cost: float
class UsageOut(BaseModel):
    username: str
    call_count: int
    total_tokens: int
    total_cost: float
