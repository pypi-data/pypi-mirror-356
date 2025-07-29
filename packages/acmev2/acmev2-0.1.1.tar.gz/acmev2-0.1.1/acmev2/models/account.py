from enum import Enum
from typing import Optional

import inject
from pydantic import BaseModel, ConfigDict, Field, computed_field

from .base import JoseJsonSchema
import josepy.jwk


class NewAccountRequestSchema(BaseModel):
    termsOfServiceAgreed: Optional[bool] = False
    contact: Optional[list[str]] = []
    onlyReturnExisting: Optional[bool] = False
    externalAccountBinding: Optional[JoseJsonSchema] = None


class AccountStatus(str, Enum):
    valid = "valid"
    deactivated = "deactivated"
    revoked = "revoked"


class AccountResource(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str | None = Field(exclude=True, default=None)

    status: AccountStatus = AccountStatus.valid
    contact: Optional[list[str]] = []
    termsOfServiceAgreed: bool
    contact: Optional[list[str]] = []
    jwk: josepy.jwk.JWK | None = Field(exclude=True, default=None)

    @computed_field
    def orders(self) -> str:
        # avoids circular import...
        from acmev2.services import ACMEEndpoint, IDirectoryService

        return inject.instance(IDirectoryService).url_for(ACMEEndpoint.order, self.id)
