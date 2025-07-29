import re

import inject
import josepy
import josepy.jwk

from acmev2.errors import ACMEError
from acmev2.messages import NewAccountMessage
from acmev2.models import AccountResource
from acmev2.services import (
    ACMEEndpoint,
    IAccountService,
    IDirectoryService,
)
from acmev2.settings import ACMESettings

from .base import ACMEModelResponse, ACMERequestHandler
import logging

logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile("^.+@.+$")
# Caddy sends mailto:default as a email contact token
# We'll just remove that.
EMAIL_DEFAULT = "mailto:default"


class NewAccountRequestHandler(ACMERequestHandler):
    """Creates a new account or retrieves an account id if the passed in jwk matches an existing one."""

    message_type = NewAccountMessage
    settings = inject.attr(ACMESettings)

    @inject.autoparams()
    def process(
        self,
        msg: NewAccountMessage,
        directory_service: IDirectoryService,
        account_service: IAccountService,
    ):
        self.validate_embedded_jwk(msg)
        self.validate_contact(msg)

        if existing_account := account_service.get_by_jwk(jwk=msg.jwk):
            logging.debug(
                "Existing account %s found with JWK %s, returning details.",
                existing_account.id,
                msg.jwk,
            )
            return ACMEModelResponse(
                msg=existing_account,
                code=200,
                location=directory_service.url_for(
                    ACMEEndpoint.account, existing_account.id
                ),
            )

        if msg.payload.onlyReturnExisting:
            logging.debug("Account lookup by JWK %s failed", msg.jwk)
            raise ACMEError(type="accountDoesNotExist")

        self.validate_tos(msg)
        eab_kid: str = None
        if msg.payload.externalAccountBinding:
            if not self.verify_eab(msg):
                logging.debug("Unable to verify external account binding.")
                raise ACMEError(type="malformed")

            eab_kid = msg.payload.externalAccountBinding.protected_decoded.get("kid")
        elif self.settings.eab_required:
            logging.debug("EAB required but no external account binding was passed in.")
            raise ACMEError(type="externalAccountRequired")

        resource = AccountResource(
            status="valid",
            termsOfServiceAgreed=msg.payload.termsOfServiceAgreed,
            contact=msg.payload.contact,
            jwk=msg.jwk,
        )

        logging.debug("Validation successful, creating new account.")
        resource = account_service.create(resource, eab_kid)

        return ACMEModelResponse(
            msg=resource,
            code=201,
            location=directory_service.url_for(ACMEEndpoint.account, resource.id),
        )

    @inject.autoparams()
    def verify_eab(
        self, msg: NewAccountMessage, account_service: IAccountService
    ) -> bool:
        eab = msg.payload.externalAccountBinding
        # The eab contains a jwk
        eab_jwk: josepy.jwk.JWK = josepy.JWK.from_json(
            msg.payload.externalAccountBinding.payload_decoded
        )
        # The eab jwk must be the same as the outer jwk
        if msg.jwk.thumbprint() != eab_jwk.thumbprint():
            logging.debug("EAB JWK does not match the outer JWK.")
            raise ACMEError()

        jws = josepy.JWS.from_json(eab.model_dump())
        # The hmac key is pulled from the account using the passed in kid
        hmac_key = account_service.get_eab_hmac(eab.protected_decoded.get("kid"))
        if not hmac_key:
            logging.debug("HMAC key not found.")
            raise ACMEError()

        # hmac key is used to verify the eab jws
        jwk = josepy.JWK.from_json({"k": hmac_key, "kty": "oct"})

        return jws.verify(jwk)

    def validate_embedded_jwk(self, msg: NewAccountMessage):
        if not msg.has_embedded_jwk:
            raise ACMEError(detail="Embedded JWK expected.")

    def validate_contact(self, msg: NewAccountMessage):
        # Only mailto contacts are currently supported
        mailtos = [c for c in msg.payload.contact or [] if c.startswith("mailto:")]

        # Remove 'default' mailtos
        mailtos = [c for c in mailtos if c != EMAIL_DEFAULT]

        for email in mailtos:
            email = email.lstrip("mailto:").strip()

            if EMAIL_REGEX.match(email):
                continue

            raise ACMEError(
                type="unsupportedContact",
                detail=f"Contact {email} is unsupported.",
            )

    @inject.autoparams()
    def validate_tos(
        self,
        msg: NewAccountMessage,
        directory_service: IDirectoryService,
    ):
        payload = msg.payload
        if not payload.termsOfServiceAgreed:
            directory = directory_service.get_directory()
            raise ACMEError(
                type="userActionRequired",
                detail="User must agree to terms of service.",
                header_links=[
                    (
                        directory["meta"]["termsOfService"],
                        "terms-of-service",
                    )
                ],
            )
