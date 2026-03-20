import asyncio
import socket

from app.config import TIMEOUT
from app.models import CheckRequest, CheckResult, PortStatus

from .base import BaseChecker


class TcpChecker(BaseChecker):
    async def check(self, req: CheckRequest) -> CheckResult:
        try:
            conn = asyncio.open_connection(req.host, req.port)
            reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT)
            writer.close()
            await writer.wait_closed()
            return CheckResult(success=True, status=PortStatus.open)
        except asyncio.TimeoutError:
            return CheckResult(success=True, status=PortStatus.filtered, error="timeout")
        except ConnectionRefusedError:
            return CheckResult(success=True, status=PortStatus.closed, error="connection_refused")
        except Exception as e:
            return CheckResult(success=False, status=PortStatus.filtered, error=str(e))
