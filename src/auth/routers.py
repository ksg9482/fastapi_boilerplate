from fastapi import APIRouter, Depends, Request, status, HTTPException

router = APIRouter(tags=['auth'])

@router.get('/jwt')
async def get_jwt():
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)