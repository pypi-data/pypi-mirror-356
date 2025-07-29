from enum import Enum

import inject
from pydantic import Field, computed_field, model_serializer

from .base import ACMEResource, RFC3339Date


class ChallengeStatus(str, Enum):
    pending = "pending"
    valid = "valid"
    invalid = "invalid"
    processing = "processing"


class ChallengeType(str, Enum):
    none = "none"
    custom = "custom"
    http_01 = "http-01"


class ChallengeResource(ACMEResource):
    id: str | None = Field(exclude=True, default=None)
    authz_id: str | None = Field(exclude=True, default=None)
    type: ChallengeType = ChallengeType.none
    token: str
    status: ChallengeStatus = ChallengeStatus.pending
    validated: RFC3339Date | None = None

    @computed_field
    @property
    def url(self) -> str:
        from acmev2.services import ACMEEndpoint, IDirectoryService

        return inject.instance(IDirectoryService).url_for(
            ACMEEndpoint.challenge, self.id
        )

    @model_serializer(mode="wrap")
    def serialize(self, handler):
        result = handler(self)
        if self.status != ChallengeStatus.valid:
            del result["validated"]

        return result


class CustomChallengeResource(ChallengeResource):
    type: ChallengeType = ChallengeType.custom


class HTTPChallengeResource(ChallengeResource):
    type: ChallengeType = ChallengeType.http_01


ChallengeResource = CustomChallengeResource | HTTPChallengeResource
