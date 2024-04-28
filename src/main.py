from fastapi import FastAPI, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn

from src.auth.middleware import get_current_user


app = FastAPI()

@app.get('/')
async def hello():
    return {"message": "hello"} 

@app.get('/jwt')
async def get_jwt():
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=get_current_user)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8083, reload=True, reload_dirs=["src"])