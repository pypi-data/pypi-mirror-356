from enum import Enum

from pydantic import Field

from .base import ACMEResource


class IdentifierType(str, Enum):
    dns = "dns"


class Identifier(ACMEResource):
    id: int | None = Field(exclude=True, default=None)
    type: IdentifierType
    value: str
