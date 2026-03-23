import logging

_formatter = logging.Formatter("%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)

for _name in ("uvicorn.access", "uvicorn.error"):
    _logger = logging.getLogger(_name)
    _logger.handlers = [_handler]
    _logger.propagate = False

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware import RateLimitMiddleware
from app.router import router

app = FastAPI(
    title="NetCheck API",
    description="TCP/UDP 포트 상태 확인 서비스",
    version="0.1.0",
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://daeho.ro", "https://*.daeho.ro"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(router, prefix="/netcheck")
