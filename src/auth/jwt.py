from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from src.auth.schemas import Token, TokenData, User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30분
REFRESH_TOKEN_EXPIRE_MINUTES = 1440 # 하루
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

"""
타입 어노테이션 -> 변수, 함수인자, 반환 값의 기대되는 데이터 타입을 명시적으로 선언하는 방법
파이썬 3.5에서 도입.

Annotated: 유형에 상황별 메타데이터를 추가
"""
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class UserInDB(User):
    hashed_password: str

# 단방향 암호화 -> 비가역적.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# CryptContext로 암호화 한 비밀번호 검증
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 암호화
def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def authenticate_user(fake_db, username: str, password: str):
    # 유저이름으로 유저 검색
    user = get_user(fake_db, username)
    # 유저가 없으면 거부
    if not user:
        return False
    # 입력한 비밀번호와 해시한 비밀번호가 같지 않으면 거부
    if not verify_password(password, user.hashed_password):
        return False
    return user
    
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    # 객체에 조작을 하게됨 -> 복사해서 불변성 유지
    to_encode = data.copy()

    # 현재시간 + 추가시간(입력시)으로 토큰 만료 기한 설정
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 추가시간 기본 15분. None을 기본으로 할거면 그냥 15분을 기본 할당으로 둬도 될거 같은데?
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    # 딕셔너리에 입력은 update메서드로 넣는게 정석
    to_encode.update({"exp": expire})

    # 데이터 + 시그니처 검증용 비밀키 + 암호화 알고리즘
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class JWTUtil:
    def __init__(self) -> None:
        pass