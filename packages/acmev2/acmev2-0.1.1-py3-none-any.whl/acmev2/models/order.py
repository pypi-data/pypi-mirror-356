from enum import Enum

import inject
from pydantic import BaseModel, Field, computed_field, field_serializer

from . import Identifier, AuthorizationResource
from .base import ACMEResource, RFC3339Date


class NewOrderRequestSchema(BaseModel):
    identifiers: list[Identifier]
    # notbefore and notafter are ignored


class OrderFinalizationRequestSchema(BaseModel):
    csr: str


class OrderStatus(str, Enum):
    pending = "pending"
    ready = "ready"
    processing = "processing"
    valid = "valid"
    invalid = "invalid"


class WithFinalizeLink:
    @computed_field
    @property
    def finalize(self: "OrderResource") -> str:
        # avoids circular import...
        from acmev2.services import ACMEEndpoint, IDirectoryService

        return inject.instance(IDirectoryService).url_for(
            ACMEEndpoint.finalize, self.id
        )


class WithCertificateLink:
    @computed_field
    @property
    def certificate(self: "OrderResource") -> str:
        """
        This field is technically optional, but some clients require it to exist. If the cert
        does not exist those clients will try to contact a non-existant url to get the cert
        and will error at retrieval.
        """
        # avoids circular import...
        from acmev2.services import ACMEEndpoint, IDirectoryService

        return inject.instance(IDirectoryService).url_for(ACMEEndpoint.cert, self.id)


class OrderResource(ACMEResource, WithFinalizeLink, WithCertificateLink):
    id: str | None = Field(exclude=True, default=None)
    account_id: str | None = Field(exclude=True, default=None)

    status: OrderStatus = OrderStatus.pending
    expires: RFC3339Date
    identifiers: list[Identifier]
    authorizations: list[AuthorizationResource]
    _mask_processing_status: bool = False

    @field_serializer("status")
    def serialize_status(self, status: OrderStatus, _info):
        # If the client does not support the "processing" state we can trick it
        # into thinking the order is still pending. This is a very specific compensation
        # to fix misbehaving clients, i.e. https://github.com/cert-manager/cert-manager/issues/5062
        if self._mask_processing_status and status == OrderStatus.processing:
            return OrderStatus.pending

        return status

    @field_serializer("authorizations")
    def serialize_authorizations(
        self, authorizations: list[AuthorizationResource], _info
    ):
        from acmev2.services import IDirectoryService, ACMEEndpoint

        directory_service = inject.instance(IDirectoryService)

        return [
            directory_service.url_for(ACMEEndpoint.authz, a.id) for a in authorizations
        ]
