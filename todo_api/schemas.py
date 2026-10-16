from pydantic import BaseModel,Field

class RegisterIn(BaseModel):
    username: str = Field(min_length=3,max_length=20)
    password: str = Field(min_length=8,max_length=72)

class UserOut(BaseModel):
    id: int
    username: str

class LoginIn(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"