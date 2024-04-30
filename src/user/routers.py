from fastapi import APIRouter, Depends, Request, status
from src.user.schemas import UserDelete, UserDeleteResponse, UserEdit, UserEditResponse
from src.user.services import UserService, get_user_service

router = APIRouter(prefix='/users', tags=['users'])

@router.put('/edit', status_code=status.HTTP_200_OK, tags=['users'], response_model=UserEditResponse)
async def update_user(request: Request, edit_user: UserEdit, service: UserService = Depends()):
    user_id = request.state.user['id']
    
    edited_user = await service.edit_user(id=user_id,password=edit_user.password, username=edit_user.username, new_password=edit_user.new_password)
    return edited_user

@router.put('/delete', status_code=status.HTTP_200_OK, tags=['users'], response_model=UserDeleteResponse)
async def update_user(request: Request, userDelete: UserDelete ,service: UserService = Depends()):
    user_id = request.state.user['id']
    
    deleted_user = await service.delete_user(user_id, userDelete.password)
    return deleted_user
