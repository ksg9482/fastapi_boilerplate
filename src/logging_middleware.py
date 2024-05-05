from datetime import datetime
import logging
from typing import List, Optional
from pydantic import Field, BaseModel
from starlette.background import BackgroundTask
from fastapi import Response, Request
import json

from src.database import get_mongodb_collection


logging.basicConfig(filename='info.log', level=logging.INFO)

class logging_form:
    def __init__(self, now, method, url, req_body, status_code, res_body):
        self.now = now
        self.method = method
        self.url = url
        self.req_body = req_body
        self.status_code = status_code
        self.res_body = res_body

    def __str__(self):
        return f"Time: {self.now} - Method: {self.method} - URL: {self.url} - Request_Body: {self.req_body} - Response_Status_Code: {self.status_code} - Response_Body: {self.res_body}"

def log_info(now, method, url, req_body, status_code, res_body):
    log = logging_form(now, method, url, req_body, status_code, res_body)
    logging.info(log.__str__())

class LogModel(BaseModel):

    # Use a string for _id, instead of ObjectID:
    id: Optional[str] = Field(default=None, description="MongoDB document ObjectID")
    time: datetime = Field(datetime, description="The time the log was created.")
    method: str = Field(str)
    url: str = Field(str)
    req_body: str = Field(str)
    res_status_code: int = Field(int)
    res_body: str = Field(str)

# @app.middleware('http') # 미들웨어로 완전 분리 필요.
async def logging_middleware(request: Request, call_next):
    """
    - User ID - 마스킹 필요
    - 접속 IP - 마스킹 필요
    - 접근한 API URL
    - Request Data
    - Response Status Code
    - 로그의 보관기간(TTL)은 60일 입니다.
    시간
    """
    method = request.method
    url = str(request.url)
    req_body = await request.body()
    response = await call_next(request)


    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk

    now = datetime.now()
    status_code = response.status_code
    task = BackgroundTask(log_info, now, method, url, req_body, status_code, res_body)
    collection = get_mongodb_collection()
    
    log = logging_form(now, method, url, json.dumps(req_body.decode('utf-8')), status_code, json.dumps(res_body.decode('utf-8')))

    logmodel = LogModel()
    logmodel.time=log.now
    logmodel.method=log.method
    logmodel.url=log.url
    logmodel.req_body=log.req_body
    logmodel.res_status_code=log.status_code
    logmodel.res_body=log.res_body

    await collection.insert_one({
        "time": logmodel.time,
        "method": logmodel.method,
        "url": logmodel.url,
        "req_body": logmodel.req_body,
        "res_status_code": logmodel.res_status_code,
        "res_body": logmodel.res_body
    })
    return Response(content=res_body, status_code=response.status_code,
                    headers=dict(response.headers), media_type=response.media_type, background=task)
