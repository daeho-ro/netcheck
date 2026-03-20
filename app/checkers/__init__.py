from app.models import CheckType

from .base import BaseChecker
from .tcp import TcpChecker
from .udp import UdpChecker

CHECKER_REGISTRY: dict[CheckType, BaseChecker] = {
    CheckType.tcp: TcpChecker(),
    CheckType.udp: UdpChecker(),
}
