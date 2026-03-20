from abc import ABC, abstractmethod

from app.models import CheckRequest, CheckResult


class BaseChecker(ABC):
    @abstractmethod
    async def check(self, req: CheckRequest) -> CheckResult:
        ...
