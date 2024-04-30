from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from src.auth.schemas import AuthTokens, SignUpUser, SignUpUserResponse, AuthToken, LoginUser, LoginUserResponse
from src.user.services import UserService

router = APIRouter(tags=['auth'])

@router.get('/jwt')
async def get_jwt():
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=SignUpUserResponse,tags=['auth'])
async def signup(signup_user: SignUpUser, service: UserService = Depends()):
    created_user = await service.create_user_account(username=signup_user.username, email=signup_user.email, password=signup_user.password)
    return created_user

@router.post('/login', status_code=status.HTTP_200_OK, response_model=AuthToken, tags=['auth'])
async def login(response:Response, user_login:LoginUser, service: UserService = Depends()):
    login_tokens = await service.login(user_login.email, user_login.password)
    response.set_cookie(key="access_token",value=f"Bearer {login_tokens.access_token}", httponly=True)
    response.set_cookie(key="refresh_token",value=f"Bearer {login_tokens.refresh_token}", httponly=True)
    return login_tokens

@router.get(
        '/refresh', 
        status_code=status.HTTP_200_OK, 
        tags=['auth'], 
        response_model=AuthTokens,
        description="새로운 access_token과 refresh_token을 발급한다."
)
async def get_new_tokens(request: Request, response:Response, service: UserService = Depends()):
    old_access_token = request.cookies['access_token']
    old_refresh_token = request.cookies['refresh_token']
    new_tokens = await service.jwt_refresh(old_access_token, old_refresh_token)

    response.set_cookie(key="access_token",value=f"Bearer {new_tokens.access_token}", httponly=True)
    response.set_cookie(key="refresh_token",value=f"Bearer {new_tokens.refresh_token}", httponly=True)
    return new_tokens