from fastapi import FastAPI, HTTPException, status
import uvicorn


app = FastAPI()

@app.get('/')
async def hello():
    return {"message": "hello"} 

@app.get('/jwt')
async def get_jwt():
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)