import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)


class ResponseLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)

        if "api/v1" not in request.url.path:
            return response

        logging.info(f"API: {request.url.path} | Execution Time: {time.time() - start_time} sec")
        return response

