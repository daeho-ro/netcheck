import ipaddress
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


class CheckRequest(BaseModel):
    type: CheckType = Field(..., description="체크 타입, tcp 또는 udp")
    host: str = Field(..., example="1.2.3.4")
    port: int = Field(..., ge=1, le=65535, example=443)

    @field_validator("host")
    @classmethod
    def host_must_be_ip(cls, v: str) -> str:
        try:
            ipaddress.ip_address(v)
        except ValueError:
            raise ValueError("host must be a valid IP address")
        return v


class CheckResult(BaseModel):
    success: bool
    status: PortStatus
    error: Optional[str] = None
