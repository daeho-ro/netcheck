# NetCheck API

TCP/UDP 포트 상태를 확인하는 REST API.

## 실행

```bash
docker compose up -d
```

## 요청

`POST /check`

| 필드 | 타입 | 설명 |
|---|---|---|
| `type` | `"tcp"` \| `"udp"` | 체크 타입 |
| `host` | string | 대상 IP (도메인 불가) |
| `port` | integer | 대상 포트 (1–65535) |

## 응답

| 필드 | 타입 | 설명 |
|---|---|---|
| `success` | boolean | 소켓 처리 성공 여부 |
| `status` | `"open"` \| `"closed"` \| `"filtered"` | 포트 상태 |
| `error` | string \| null | 오류 메시지 |

`filtered` — 타임아웃. 방화벽 드롭이거나 무응답으로 open/closed 판별 불가.

