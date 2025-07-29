from enum import Enum
from typing import Optional

from pydantic import BaseModel


class NewAccountRequestSchema(BaseModel):
    termsOfServiceAgreed: Optional[bool] = False
    contact: Optional[list[str]] = None
    onlyReturnExisting: Optional[bool] = False


class AccountStatus(str, Enum):
    valid = "valid"
    deactivated = "deactivated"
    revoked = "revoked"


class ProblemResource(BaseModel):
    type: str
    detail: Optional[str] = None
