from fastapi import FastAPI, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
from src.database import Base, engine
from src.auth.middleware import get_current_user
from src.auth import routers as auth_router

async def app_lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # dev일때만. 실제로는 사용하면 안됨
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield 

app = FastAPI(
    lifespan=app_lifespan, 
    # docs_url=None, 
    # redoc_url=None
    ) 

app.include_router(auth_router.router)

@app.get('/')
async def hello():
    return {"message": "hello"} 

app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=get_current_user)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, reload_dirs=["src"])