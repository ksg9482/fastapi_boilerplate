from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from src.auth.jwt import get_user, oauth2_scheme, SECRET_KEY, ALGORITHM, fake_users_db
from src.auth.schemas import TokenData, User

# oauth2 프로토콜

# oauth2_scheme는 의존성 주입을 가져옴 -> fastapi가 의존성 관리
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        # 헤더에 auth 넣음 -> Bearer까진 넣고 그 이후는 안넣음
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # sub는 토큰의 소유자를 나타냄
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled: # 유저는 비활성화 되었지만 토큰은 유효할 수 있음. 특히 refresh_token 같은거.
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user