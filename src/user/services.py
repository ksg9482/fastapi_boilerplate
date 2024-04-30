from datetime import timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status

from src.user.dependencies import get_hashed_password
from src.user.models import User
from src.user.repository import UserRepository
from src.user.util import JwtUtils

class JWTTokens:
    def __init__(self, access_token:str, refresh_token:str):
        self.access_token = access_token
        self.refresh_token = refresh_token

class UserService:
    def __init__(self) -> None:
        repo:UserRepository=Depends(), 
        utills:JwtUtils=Depends()

    async def create_user_account(self, username: str, email: str, password: str) -> User:
        existing_user = await self.repo.find_by_email(email)
        if existing_user:
            raise HTTPException(status_code=400, detail='이미 가입된 사용자입니다.')

        hashed_password = get_hashed_password(password)
        new_user = User(username=username, email=email, password=hashed_password)
        try:
            await self.repo.save(new_user)
            return new_user
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail='회원가입이 실패했습니다. 기입한 내용을 확인해보세요')

    async def login(self, email: str, password: str):
        user = await self.repo.find_by_email(email)

        if user is None:
            raise HTTPException(status_code=400, detail='존재하지 않는 사용자입니다.')

        if self.valid_password(password, user.password) is False:
            raise HTTPException(status_code=401, detail="잘못된 비밀번호 입니다.")
        
        access_token = self.utills.encode_access_token(user.id, user.email, user.username, timedelta(hours=1))
        refresh_token = self.utills.encode_refresh_token(user.id, user.email, user.username, timedelta(hours=24))
        
        tokens = JWTTokens(access_token, refresh_token)
        return tokens
    
    async def jwt_refresh(self, access_token:str, refresh_token:str):
        access_token_valid_options = {"verify_exp": False}
        if not self.utills.decode_token(access_token, access_token_valid_options) or not self.utills.decode_token(refresh_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다.",
            )
        user = self.utills.decode_token(refresh_token)
        user_id = user['data']['id']

        finded_user = await self.repo.find_by_id(user_id)
        if finded_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='존재하지 않는 사용자입니다.')

        access_token = self.utills.encode_access_token(finded_user.id, finded_user.email, finded_user.username, timedelta(hours=1))
        refresh_token = self.utills.encode_refresh_token(finded_user.id, finded_user.email, finded_user.username, timedelta(hours=24))
        await self.repo.save_refresh_token(refresh_token)

        return {'access_token': access_token, 'refresh_token': refresh_token}