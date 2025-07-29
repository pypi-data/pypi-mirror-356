import random
import josepy
import re
import string
from datetime import datetime

import inject
import josepy
from cryptography import x509

from acmev2.errors import ACMEBadCSRDetail, ACMEBadCSRError, ACMEError
from acmev2.messages import NewOrderMessage, OrderFinalizationMessage, OrderMessage
from acmev2.models import (
    AuthorizationResource,
    AuthorizationStatus,
    HTTPChallengeResource,
    CustomChallengeResource,
    IdentifierType,
    OrderResource,
    OrderStatus,
    without,
)
from acmev2.services import (
    ACMEEndpoint,
    IAuthorizationService,
    IChallengeService,
    IDirectoryService,
    IOrderService,
)
from acmev2.settings import ACMESettings, Challenges

from .base import ACMEModelResponse, ACMERequestHandler, ACMEResponse
import logging

logger = logging.getLogger(__name__)

# Naive regex just to make sure domains have basic validation
# before the server creates authorizations. We're not worried about
# clients submitting domains that don't resolve or submitting
# malformed domains, those will error in the challenge phase.
DOMAIN_REGEX = re.compile(r"^[^-][A-Za-z0-9-\.]+[^-]$")


class ACMEOrderResponse(ACMEResponse[OrderResource]):
    settings = inject.attr(ACMESettings)

    def __init__(self, *args, **kwargs):
        user_agent = kwargs.pop("user_agent", None)
        if user_agent is None:
            raise Exception("ACMEOrderResponse MUST include user_agent parameter")

        super().__init__(*args, **kwargs)

        if re.match(self.settings.mask_order_processing_status_ua_match, user_agent):
            logging.debug(
                "Annoying client found: %s. Masking order processing as pending.",
                user_agent,
            )
            self.msg._mask_processing_status = True

    def serialize(self) -> str:
        if self.msg:
            return self.msg.model_dump_json(indent=2)
        else:
            return ""


class NewOrderRequestHandler(ACMERequestHandler):
    """Handles new order requests and creates all supported authorizations and challenges."""

    message_type = NewOrderMessage
    settings = inject.attr(ACMESettings)
    challenge_service = inject.attr(IChallengeService)
    authorization_service = inject.attr(IAuthorizationService)
    order_service = inject.attr(IOrderService)
    directory_service = inject.attr(IDirectoryService)

    def process(self, msg: NewOrderMessage):
        self.identifier_validator(msg)
        # We ignore notBefore and notAfter. I know part of the spec is
        # that we MUST NOT issue a cert with contents other than those requested,
        # but this is an internal ACME server and we know better than the clients.
        # Also our CA overriddes several of our settings anyway when we forward the
        # finalized CSR, so good luck enforcing the RFC.
        resource_expiration = datetime.now() + self.settings.resource_expiration_delta

        new_order = OrderResource(
            account_id=msg.account.id,
            expires=resource_expiration,
            identifiers=msg.payload.identifiers,
            authorizations=[],
        )

        new_order = self.order_service.create(new_order)
        for identifier in new_order.identifiers:
            authorization = AuthorizationResource(
                order_id=new_order.id,
                expires=resource_expiration,
                identifier=identifier,
            )

            authz: AuthorizationResource = self.authorization_service.create(
                authorization
            )
            new_order.authorizations.append(authz)

            for chall_type in self.settings.challenges_available:
                # The spec doesn't say this has to be base64 encoded, but
                # certbot thinks it is?
                token = josepy.encode_b64jose(
                    "".join(
                        random.choices(string.ascii_letters + string.digits, k=50)
                    ).encode()
                )
                match chall_type:
                    case Challenges.http_01:
                        chall = HTTPChallengeResource(
                            authz_id=authz.id,
                            # The spec doesn't say this has to be base64 encoded, but
                            # certbot thinks it is?
                            token=token,
                        )
                        chall = self.challenge_service.create(chall)
                        authz.challenges.append(chall)
                    case Challenges.custom:
                        chall = CustomChallengeResource(authz_id=authz.id, token=token)
                        chall = self.challenge_service.create(chall)
                        authz.challenges.append(chall)
                    case _:
                        raise Exception(
                            f"No challenge mapped to challenge type {chall_type.value}"
                        )

        return ACMEOrderResponse(
            msg=new_order,
            code=201,
            location=self.directory_service.url_for(ACMEEndpoint.order, new_order.id),
            user_agent=self.headers.get("User-Agent", ""),
        )

    def identifier_validator(self, msg: NewOrderMessage):
        logging.debug("Validating identifiers")
        if len(msg.payload.identifiers) == 0:
            logging.debug("No validators found!")
            raise ACMEError(
                type="malformed", detail="No identifiers present in payload"
            )

        if len(msg.payload.identifiers) > self.settings.max_identifiers:
            logging.debug(
                "Too many identifiers found. %s is more than %s.",
                len(msg.payload.identifiers),
                self.settings.max_identifiers,
            )
            raise ACMEError(
                type="malformed",
                detail=f"Too many identifiers. Max is {self.settings.max_identifiers}",
            )

        # All identifiers must be of type "dns" and a single well-formed domain.
        # wildcards MUST NOT be issued.
        for identifier in msg.payload.identifiers:
            if identifier.type != IdentifierType.dns:
                logging.debug(
                    "Identifiers must be DNS only. %s found.", identifier.type
                )
                raise ACMEError(
                    type="rejectedIdentifier",
                    detail=f"{identifier.type} is not supported",
                )

            if "*" in identifier.value:
                logging.debug(
                    "Invalid '*' found in identifier value %s.", identifier.value
                )
                raise ACMEError(
                    type="rejectedIdentifier",
                    detail="Wildcard identifiers are not supported",
                )

            if not DOMAIN_REGEX.match(identifier.value):
                logging.debug(
                    "Domain regex %s did not match %s.",
                    DOMAIN_REGEX.pattern,
                    identifier.value,
                )
                raise ACMEError(
                    type="rejectedIdentifier",
                    detail=f"{identifier.value} is formatted incorrectly",
                )

            for domain_regex in self.settings.blacklisted_domains:
                if re.match(domain_regex, identifier.value):
                    logging.debug(
                        "Identifier %s was blocked by regex %s",
                        identifier.value,
                        domain_regex,
                    )
                    raise ACMEError(
                        type="rejectedIdentifier",
                        detail=f"{identifier.value} is not allowed",
                    )


class OrderFinalizationRequestHandler(ACMERequestHandler):
    """Order finalization is performed when all authorizations are valid and the client
    wishes to submit a certificate signing request."""

    message_type = OrderFinalizationMessage
    order_service = inject.attr(IOrderService)
    directory_service = inject.attr(IDirectoryService)
    authorization_service = inject.attr(IAuthorizationService)

    def process(
        self,
        msg: OrderFinalizationMessage,
    ):
        order = self.order_service.resolve_state(msg.resource)

        if order.status != OrderStatus.ready:
            logging.debug(
                "Order %s was attempted to be finalized when it was not ready.",
                order.id,
            )
            raise ACMEError(type="orderNotReady")

        # This probably never gets hit, the resolve_state method above should force orders
        # to an invalid state if they're expired.
        self.validate_expiration(order)
        self.validate_authorizations(order)

        csr = x509.load_der_x509_csr(josepy.decode_b64jose(msg.payload.csr))
        self.validate_identifiers(order, csr)

        order = self.order_service.process_finalization(order, csr)

        order_without_links = without(order, ["certificate", "finalize"])

        return ACMEOrderResponse(
            msg=order_without_links,
            code=200,
            user_agent=self.headers.get("User-Agent", ""),
        )

    def validate_expiration(self, order: OrderResource):
        if datetime.now() > order.expires:
            logging.debug("Attempting to process expired order %s", order.id)
            raise ACMEError(detail="Order has expired")

    def validate_authorizations(self, order: OrderResource):
        authz_status = [
            a.status == AuthorizationStatus.valid for a in order.authorizations
        ]

        if not all(authz_status):
            logging.debug("Not all authorizations for order %s are valid", order.id)
            raise ACMEBadCSRError(ACMEBadCSRDetail.orderNotAuthorized)

    def validate_identifiers(
        self, order: OrderResource, csr: x509.CertificateSigningRequest
    ):
        cn: str = None
        try:
            cn: str = csr.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value
        except IndexError:
            # Some clients don't pass a CN, we can use the first SAN in that case
            cn = None

        sans: list[str] = []

        try:
            sans_ext = csr.extensions.get_extension_for_oid(
                x509.OID_SUBJECT_ALTERNATIVE_NAME
            )
        except x509.ExtensionNotFound:
            raise ACMEBadCSRError(ACMEBadCSRDetail.sansRequired)

        for san in sans_ext.value:
            if not isinstance(san, x509.DNSName):
                raise ACMEBadCSRError(ACMEBadCSRDetail.invalidSan)
            sans.append(san.value)

        if cn is None:
            cn = sans[0]

        if cn not in sans:
            raise ACMEBadCSRError(ACMEBadCSRDetail.cnMissingFromSan)

        csr_domains = {cn} | set(sans)
        order_identifiers = set(i.value for i in order.identifiers)

        if csr_domains != order_identifiers:
            raise ACMEBadCSRError(ACMEBadCSRDetail.csrOrderMismatch)


class OrderRequestHandler(ACMERequestHandler):
    """Returns the order resource with links to all authorizations."""

    message_type = OrderMessage
    order_service = inject.attr(IOrderService)
    directory_service = inject.attr(IDirectoryService)
    authorization_service = inject.attr(IAuthorizationService)

    def process(
        self,
        msg: OrderMessage,
    ):
        order = self.order_service.resolve_state(msg.resource)

        return ACMEOrderResponse(
            msg=order,
            code=200,
            location=self.directory_service.url_for(ACMEEndpoint.order, order.id),
            user_agent=self.headers.get("User-Agent", ""),
        )
