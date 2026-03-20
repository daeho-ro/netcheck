import time
from collections import defaultdict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

_last_seen: dict[str, float] = defaultdict(float)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        ip = request.client.host if request.client else "unknown"
        now = time.monotonic()

        if now - _last_seen[ip] < 1.0:
            return Response(content="Too Many Requests", status_code=429)

        _last_seen[ip] = now
        return await call_next(request)
