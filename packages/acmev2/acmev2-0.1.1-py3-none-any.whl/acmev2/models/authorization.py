from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from acmev2.models.challenge import CustomChallengeResource, HTTPChallengeResource

from . import Identifier
from .base import RFC3339Date


class AuthorizationStatus(str, Enum):
    """https://datatracker.ietf.org/doc/html/rfc8555/#section-7.1.6"""

    pending = "pending"
    valid = "valid"
    invalid = "invalid"
    deactivated = "deactivated"
    expired = "expired"
    revoked = "revoked"


class AuthorizationSchema(BaseModel):
    status: Optional[AuthorizationStatus] = None


class AuthorizationResource(BaseModel):
    id: str | None = Field(exclude=True, default=None)
    order_id: str | None = Field(exclude=True, default=None)

    status: AuthorizationStatus = AuthorizationStatus.pending
    expires: RFC3339Date
    identifier: Identifier
    challenges: list[HTTPChallengeResource | CustomChallengeResource] = []
