import asyncio
import socket

from app.config import TIMEOUT
from app.models import CheckRequest, CheckResult, PortStatus

from .base import BaseChecker


class UdpChecker(BaseChecker):
    _PAYLOAD = b"\x00"

    async def check(self, req: CheckRequest) -> CheckResult:
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._probe, req.host, req.port, TIMEOUT)
        except Exception as e:
            return CheckResult(success=False, status=PortStatus.filtered, error=str(e))

    def _probe(self, host: str, port: int, timeout: float) -> CheckResult:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        try:
            sock.sendto(self._PAYLOAD, (host, port))
            try:
                sock.recvfrom(1024)
                return CheckResult(success=True, status=PortStatus.open)
            except socket.timeout:
                return CheckResult(success=True, status=PortStatus.filtered, error="no_response")
        except ConnectionRefusedError:
            return CheckResult(success=True, status=PortStatus.closed, error="icmp_port_unreachable")
        except Exception as e:
            return CheckResult(success=False, status=PortStatus.filtered, error=str(e))
        finally:
            sock.close()
