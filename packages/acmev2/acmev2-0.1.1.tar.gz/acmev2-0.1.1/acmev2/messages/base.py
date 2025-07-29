from typing import Any, Generic, Mapping, Self, TypeVar
import typing

import inject
import josepy
from acmev2.errors import (
    ACMEError,
    ACMEBadNonceError,
    ACMEMalformedError,
    ACMEResourceNotFoundError,
    ACMESignatureVerificationError,
    ACMEUnauthorizedError,
)
from acmev2.models import JoseJsonSchema, EmptyMessageSchema, AccountResource
from pydantic import ValidationError, BaseModel
from acmev2.services import (
    IAccountService,
    ACMEEndpoint,
    ACMEResourceType,
    IDirectoryService,
    IOrderService,
    IChallengeService,
    IAuthorizationService,
    ICertService,
)
import logging

logger = logging.getLogger(__name__)

R = TypeVar("R", bound=BaseModel)
T = TypeVar("T", bound=BaseModel)


class ACMEMessage:

    body: Mapping[str, Any] = None

    def __init__(self, body: Mapping[str, Any]):
        self.body = body

    @property
    def nonce(self) -> str | None:
        return None

    @classmethod
    def from_json(cls, body: Mapping[str, Any]) -> Self:
        return cls(body)


class SignedACMEMessage(ACMEMessage, Generic[T]):
    has_nonce: True
    schema: T = EmptyMessageSchema

    _payload: T = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Awkward way to set the schema with the generic type
        bases = typing.get_args(self.__orig_bases__[0])
        if len(bases) > 0:
            self.schema = bases[0]

    @classmethod
    def from_json(cls, body: Mapping[str, Any]) -> Self:
        msg = cls(body)
        # All signed messages must have a body with a header, payload, and signature
        try:
            JoseJsonSchema.model_validate(body)
        except ValidationError as exc:
            raise ACMEMalformedError(exc)

        if not msg.verify_signature():
            raise ACMESignatureVerificationError()

        # There must be a "nonce" entry in the protected header
        if "nonce" not in msg.jose_message.protected_decoded:
            raise ACMEBadNonceError()

        return msg

    @property
    def nonce(self) -> str | None:
        return self.jose_message.protected_decoded["nonce"]

    @property
    def url(self) -> str | None:
        return self.jose_message.protected_decoded["url"]

    @property
    def payload(self) -> T:
        if not self._payload:
            self._payload = self.schema(**self.jose_message.payload_decoded)

        return self._payload

    _jose_message: JoseJsonSchema = None

    @property
    def jose_message(self) -> JoseJsonSchema:
        if not self._jose_message:
            try:
                self._jose_message = JoseJsonSchema(**dict(self.body))
            except ValidationError as exc:
                # Error in the body format
                raise ACMEMalformedError(exc)

        return self._jose_message

    _jws: josepy.JWS = None

    @property
    def jws(self) -> josepy.JWS:
        if not self._jws:
            self._jws = josepy.JWS.from_json(self.body)

        return self._jws

    _jwk: josepy.JWK = None

    @property
    def has_embedded_jwk(self) -> bool:
        return "jwk" in self.jose_message.protected_decoded

    @property
    def has_kid(self) -> bool:
        return "kid" in self.jose_message.protected_decoded

    @property
    @inject.autoparams()
    def jwk(self, account_service: IAccountService) -> josepy.JWK:
        if not self._jwk:
            if self.has_embedded_jwk and self.has_kid:
                raise ACMEError(type="malformed")

            protected = self.jose_message.protected_decoded
            if self.has_kid:
                if isinstance(self, AuthenticatedACMEMessage):
                    jwk = self.account.jwk if self.account else None
                else:
                    jwk = account_service.get(protected["kid"]).jwk

                if not jwk:
                    raise ACMEError(type="accountDoesNotExist")

                self._jwk = jwk
            else:
                self._jwk = josepy.JWK.from_json(protected["jwk"])

        return self._jwk

    def verify_signature(self) -> bool:
        return self.jws.verify(self.jwk)


class AuthenticatedACMEMessage:
    @property
    def account_id(self: SignedACMEMessage | Self) -> str:
        return self.jose_message.protected_decoded["kid"]

    _account: AccountResource | None = None

    @property
    def account(self: SignedACMEMessage | Self) -> AccountResource | None:
        if not self._account:
            auth_service = inject.instance(IAccountService)
            directory_service = inject.instance(IDirectoryService)
            account_identifier = directory_service.identifier_from_url(
                ACMEEndpoint.account, self.account_id
            )
            if not account_identifier:
                logger.error(
                    "Failed to extract account identifier from id: %s", self.account_id
                )

            self._account = auth_service.get(account_identifier)

        return self._account


class WithResourceUrl(Generic[R], AuthenticatedACMEMessage):

    protected_resource_type: ACMEResourceType
    protected_url_type: ACMEEndpoint

    @property
    def resource(self: SignedACMEMessage | Self) -> R:
        directory_service = inject.instance(IDirectoryService)
        account_service = inject.instance(IAccountService)

        resource_id = directory_service.identifier_from_url(
            self.protected_url_type, self.url
        )

        if not resource_id:
            raise ACMEResourceNotFoundError()

        concrete_resource: R = None
        match self.protected_resource_type:
            case ACMEResourceType.order:
                concrete_resource = inject.instance(IOrderService).get(resource_id)
            case ACMEResourceType.authz:
                concrete_resource = inject.instance(IAuthorizationService).get(
                    resource_id
                )
            case ACMEResourceType.challenge:
                concrete_resource = inject.instance(IChallengeService).get(resource_id)
            case ACMEResourceType.cert:
                concrete_resource = inject.instance(ICertService).get(resource_id)
            case _:
                raise Exception(
                    f"Could not get resource from type {self.protected_resource_type}"
                )

        if not concrete_resource:
            raise ACMEResourceNotFoundError()

        if not account_service.check_access(
            self.account.id, resource_id, self.protected_resource_type
        ):
            raise ACMEUnauthorizedError()

        return concrete_resource
