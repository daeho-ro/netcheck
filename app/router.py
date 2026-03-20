from fastapi import APIRouter, Request

from app.checkers import CHECKER_REGISTRY
from app.models import CheckRequest, CheckResult

router = APIRouter()


@router.get("/ip")
async def client_ip(request: Request) -> dict:
    return {"ip": request.client.host if request.client else None}


@router.post("/check", response_model=CheckResult)
async def check(request: Request, req: CheckRequest) -> CheckResult:
    return await CHECKER_REGISTRY[req.type].check(req)
