from collections import defaultdict
import random
import string
from typing import Mapping
import uuid

from cryptography.x509 import Certificate, CertificateSigningRequest
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
import inject
from josepy.jwk import JWK

from acmev2.errors import ACMEError
from acmev2.models import (
    AccountResource,
    OrderResource,
    AuthorizationResource,
    HTTPChallengeResource,
    CustomChallengeResource,
    ChallengeResource,
    ChallengeStatus,
    OrderStatus,
    CertResource,
)
from acmev2.services import (
    IDirectoryService,
    INonceService,
    IAccountService,
    IOrderService,
    IAuthorizationService,
    IChallengeService,
)
from acmev2.services import ACMEEndpoint, ACMEResourceType
from datetime import datetime, timedelta, timezone

from acmev2.services.services import ICertService


class MemoryDirectoryService(IDirectoryService):
    root_url = "http://acme.localhost/acme"
    external_account_required = False

    def url_base(self) -> str:
        return self.root_url


class MemoryNonceService(INonceService):

    nonces = []

    def __init__(self):
        self.nonces = []

    def generate(self) -> str:
        nonce = uuid.uuid4().hex
        self.nonces.append(nonce)

        return nonce

    def consume(self, nonce: str) -> bool:
        if nonce in self.nonces:
            self.nonces.remove(nonce)
            return True

        return False


AccountIdStr = str
KIDStr = str
HMACStr = str


class MemoryAccountService(IAccountService):

    accounts: Mapping[AccountIdStr, tuple[AccountResource, JWK]] = {}
    hmacs: Mapping[KIDStr, HMACStr] = {}
    bound_accounts: Mapping[KIDStr, AccountIdStr] = {}
    order_service = inject.attr(IOrderService)
    account_service = inject.attr(IAccountService)
    directory_service = inject.attr(IDirectoryService)
    authz_service = inject.attr(IAuthorizationService)

    def __init__(self):
        self.accounts = {}
        self.hmacs = {}
        self.bound_accounts = {}

    def gen_hmac(self) -> tuple[KIDStr, HMACStr]:
        kid = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        hmac = "".join(random.choices(string.ascii_letters + string.digits, k=10))

        self.hmacs[kid] = hmac

        return (kid, hmac)

    def create(self, resource: AccountResource, eab_kid: str = None) -> AccountResource:
        if eab_kid and eab_kid in self.bound_accounts:
            raise ACMEError(
                type="malformed",
                detail="Client may not reuse external account bindings",
            )

        while account_id := "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        ):
            if account_id not in self.accounts:
                break

        resource.id = account_id
        self.accounts[resource.id] = (resource, resource.jwk)

        if eab_kid:
            self.bound_accounts[eab_kid] = resource.id

        return resource

    def get(self, account_id: str) -> AccountResource | None:
        try:
            return self.accounts.get(account_id)[0]
        except:
            return None

    def get_by_jwk(self, jwk: JWK) -> AccountResource | None:
        for acct, acct_jwk in self.accounts.values():
            if jwk.thumbprint() == acct_jwk.thumbprint():
                return acct

    def get_eab_hmac(self, kid: str) -> str | None:
        return self.hmacs.get(kid)

    def check_access(
        self, account_id: str, resource_id: str, resource_type: ACMEResourceType
    ) -> bool:
        # Perms will be done out of band, so we're going to bypass services and
        # just cast to what they are
        order_service: MemoryOrderService = self.order_service
        account_service: MemoryAccountService = self.account_service

        match resource_type:
            case ACMEResourceType.authz:
                for order in order_service.account_orders[account_id]:
                    for auth in order_service.orders[order.id].authorizations:
                        if auth.id == resource_id:
                            return True

                return False
            case ACMEResourceType.challenge:
                for order in order_service.account_orders[account_id]:
                    for auth in order_service.orders[order.id].authorizations:
                        if not auth:
                            continue
                        for chall in auth.challenges:
                            if chall.id == resource_id:
                                return True  # whew

                return False
            case ACMEResourceType.order | ACMEResourceType.cert:
                for order in order_service.account_orders.get(account_id, []):
                    if order.id == resource_id:
                        return True

                return False

            case _:
                return False


OrderIdStr = str


class MemoryOrderService(IOrderService):

    account_orders: Mapping[AccountIdStr, list[OrderResource]] = defaultdict(list)
    orders: Mapping[OrderIdStr, OrderResource] = {}
    order_csrs: Mapping[OrderIdStr, CertificateSigningRequest] = defaultdict(dict)
    authorization_service = inject.attr(IAuthorizationService)

    def __init__(self):
        self.account_orders = defaultdict(list)
        self.orders = {}
        self.order_csrs = defaultdict(dict)

    def create(self, resource: OrderResource) -> OrderResource:
        if not resource.id:
            while order_id := "".join(
                random.choices(string.ascii_letters + string.digits, k=10)
            ):
                if order_id not in self.orders:
                    break

            resource.id = order_id

        self.orders[resource.id] = resource
        self.account_orders[resource.account_id].append(resource)

        return resource

    def update_status(self, order, new_state):
        order.status = new_state
        return order

    def get(self, order_id: str) -> OrderResource | None:
        return self.orders.get(order_id)

    def process_finalization(
        self, order: OrderResource, csr: CertificateSigningRequest
    ) -> OrderResource:
        order.status = OrderStatus.processing
        self.order_csrs[order.id] = csr
        return order


AuthzIdStr = str


class MemoryAuthorizationService(IAuthorizationService):

    authorizations: Mapping[AuthzIdStr, AuthorizationResource] = {}
    challenge_service = inject.attr(IChallengeService)
    directory_service = inject.attr(IDirectoryService)
    order_service = inject.attr(IOrderService)
    authz_service = inject.attr(IAuthorizationService)

    def __init__(self):
        self.authorizations = {}

    def create(self, authz: AuthorizationResource) -> AuthorizationResource:
        if authz.id is None:
            while authz_id := "".join(
                random.choices(string.ascii_letters + string.digits, k=10)
            ):
                if authz_id not in self.authorizations:
                    break

            authz.id = authz_id

        self.authorizations[authz.id] = authz

        return authz

    def update_status(self, authz, new_state):
        authz.status = new_state
        return authz

    def get(self, authz_id: str) -> AuthorizationResource | None:
        return self.authorizations.get(authz_id)

    def get_by_order(self, order_id: str) -> list[AuthorizationResource]:
        order_service: MemoryOrderService = self.order_service
        authorizations: list[AuthorizationResource] = []
        for auth_url in order_service.orders[order_id].authorizations:
            authz_id = self.directory_service.identifier_from_url(
                ACMEEndpoint.authz, auth_url
            )
            authorizations.append(self.authz_service.get(authz_id))

        return authorizations

    def get_by_chall(self, chall_id: str) -> AuthorizationResource | None:
        for _, auth in self.authorizations.items():
            for chall in auth.challenges:
                if chall.id == chall_id:
                    return auth


ChallengeIdStr = str


class MemoryChallengeService(IChallengeService):

    challenges: Mapping[
        ChallengeIdStr, HTTPChallengeResource | CustomChallengeResource
    ] = {}
    directory_service = inject.attr(IDirectoryService)
    authorization_service = inject.attr(IAuthorizationService)

    def __init__(self):
        self.challenges = {}

    def create(self, chall: ChallengeResource) -> list[ChallengeResource]:
        if not chall.id:
            while chall_id := "".join(
                random.choices(string.ascii_letters + string.digits, k=10)
            ):
                if chall_id not in self.challenges:
                    break

            chall.id = chall_id

        self.challenges[chall.id] = chall

        return chall

    def update_status(self, chall, new_state):
        if chall.status != new_state and new_state == ChallengeStatus.valid:
            chall.validated = datetime.now()
        chall.status = new_state

        return chall

    def get(self, chall_id: str) -> ChallengeResource:
        return self.challenges.get(chall_id)

    def queue_validation(self, chall: ChallengeResource) -> ChallengeResource:
        return chall


CA_KEY = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

CA_SUBJ = CA_ISSUER = x509.Name(
    [
        x509.NameAttribute(x509.NameOID.COMMON_NAME, "acmeca.local"),
    ]
)
CA_CERT = (
    x509.CertificateBuilder()
    .subject_name(CA_SUBJ)
    .issuer_name(CA_ISSUER)
    .public_key(CA_KEY.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.now(timezone.utc))
    .not_valid_after(
        # Our certificate will be valid for 10 days
        datetime.now(timezone.utc)
        + timedelta(days=10)
    )
    .add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]),
        critical=False,
        # Sign our certificate with our private key
    )
    .sign(CA_KEY, hashes.SHA256())
)


class MemoryCertService(ICertService):
    order_service: MemoryOrderService = inject.attr(IOrderService)

    def get(self, ord_id: str) -> CertResource | None:
        csr = self.order_service.order_csrs.get(ord_id)
        if csr:
            builder = (
                x509.CertificateBuilder()
                .subject_name(csr.subject)
                .issuer_name(CA_CERT.issuer)
                .public_key(csr.public_key())
                .serial_number(x509.random_serial_number())
                .not_valid_before(datetime.now(timezone.utc))
                .not_valid_after(datetime.now(timezone.utc) + timedelta(days=90))
            )

            for ext in csr.extensions:
                builder = builder.add_extension(ext.value, ext.critical)

            cert = builder.sign(CA_KEY, hashes.SHA256())

            return CertResource(
                pem=cert.public_bytes(serialization.Encoding.PEM)
                + CA_CERT.public_bytes(serialization.Encoding.PEM)
            )
