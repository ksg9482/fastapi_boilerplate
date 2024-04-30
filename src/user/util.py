from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import timedelta, datetime

JWT_SECRET_KEY = '}NTg5t[S`{WNmI00Ri$+:O67[NWEiB'
JWT_ALGORITHM = 'HS256'

class JwtUtils:
    def encode_access_token(self, id:int, email:str, username:str, timedelta:timedelta=timedelta(hours=1)):
        if all([id, email, username]):
            payload = {
                'exp': datetime.now() + timedelta,
                'iat': datetime.now(),
                'scope': 'access_token',
                'data': {
                    'id': id,
                    'email': email,
                    'username': username
                }
            }
            return jwt.encode(
                payload,
                JWT_SECRET_KEY,
                algorithm=JWT_ALGORITHM
            )
        else:
            raise ValueError("Invalid parameters")
    

    def encode_refresh_token(self, id:int, email:str, username:str, timedelta:timedelta=timedelta(hours=24)):
        if all([id, email, username]):
            payload = {
                'exp': datetime.now() + timedelta,
                'iat': datetime.now(),
                'scope': 'refresh_token',
                'data': {
                    'id': id,
                    'email': email,
                    'username': username
                }
            }
            return jwt.encode(
                payload,
                JWT_SECRET_KEY,
                algorithm=JWT_ALGORITHM
            )
        else:
            raise ValueError("Invalid parameters")

    def decode_token(self, token:str, options:Optional[dict]=None):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], options=options)
            return payload
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
def get_user_utills(utills: JwtUtils=Depends(JwtUtils)):
    return utills