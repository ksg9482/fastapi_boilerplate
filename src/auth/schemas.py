from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None # 유저 활성화 여부

class SignUpUser(BaseModel):
    email: str
    password: str
    username: str

class SignUpUserResponse(BaseModel):
    email: str
    username: str

class LoginUser(BaseModel):
    email: str
    password: str

class LoginUserResponse(BaseModel):
    email: str

class AuthToken(BaseModel):
    access_token: str