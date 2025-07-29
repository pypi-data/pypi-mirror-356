from pydantic import Field
from .base import ACMEResource


class CertResource(ACMEResource):
    id: str | None = Field(exclude=True, default=None)
    pem: str
