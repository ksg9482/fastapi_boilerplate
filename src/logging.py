from datetime import datetime
import logging
from starlette.background import BackgroundTask

from fastapi import Response, Request


logging.basicConfig(filename='info.log', level=logging.INFO)

# request log 객체와 response log 객체로 관리하자.
def log_info(now, method, url, req_body, status_code, res_body):
    logging.info(now)
    logging.info(method)
    logging.info(url)
    logging.info(req_body)
    logging.info(status_code)
    logging.info(res_body)


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
    print(request.__dict__)
    method = request.method
    url = request.url
    req_body = await request.body()
    response = await call_next(request)


    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk

    now = datetime.now()
    status_code = response.status_code
    task = BackgroundTask(log_info, now, method, url ,req_body, status_code, res_body)
    return Response(content=res_body, status_code=response.status_code,
                    headers=dict(response.headers), media_type=response.media_type, background=task)
