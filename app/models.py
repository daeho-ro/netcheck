import ipaddress
import re
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class CheckType(str, Enum):
    tcp = "tcp"
    udp = "udp"


class PortStatus(str, Enum):
    open     = "open"      # TCP: 연결 성공 / UDP: 응답 수신
    closed   = "closed"    # TCP: RST(connection_refused) / UDP: ICMP Port Unreachable
    filtered = "filtered"  # TCP/UDP: 타임아웃 (방화벽 드롭 또는 무응답)


_HOSTNAME_LABEL = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$")


def _is_valid_hostname(v: str) -> bool:
    if not v or len(v) > 253:
        return False
    hostname = v.rstrip(".")
    return all(_HOSTNAME_LABEL.match(label) for label in hostname.split("."))


class CheckRequest(BaseModel):
    type: CheckType = Field(..., description="체크 타입, tcp 또는 udp")
    host: str = Field(..., example="example.com")
    port: int = Field(..., ge=1, le=65535, example=443)

    @field_validator("host")
    @classmethod
    def host_must_be_ip_or_hostname(cls, v: str) -> str:
        try:
            ipaddress.ip_address(v)
            return v
        except ValueError:
            pass
        if _is_valid_hostname(v):
            return v
        raise ValueError("host must be a valid IP address or hostname")


class CheckResult(BaseModel):
    success: bool
    status: PortStatus
    error: Optional[str] = None
