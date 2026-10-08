from pydantic import BaseModel,Field

class LoginIn(BaseModel):
    username: str
    password: str