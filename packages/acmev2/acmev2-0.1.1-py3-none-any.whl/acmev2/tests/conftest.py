import io
import json
import logging.config
from typing import Any, Callable, Mapping, TypedDict

import acme.jws
import acme
import acme.client
import inject
import josepy
import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

import requests.adapters
import urllib3

from acmev2.models import (
    AccountResource,
    OrderResource,
    NewAccountRequestSchema,
    NewOrderRequestSchema,
    EmptyMessageSchema,
    AuthorizationSchema,
    OrderFinalizationRequestSchema,
)
from acmev2.handlers import (
    NewNonceRequestHandler,
    NewAccountRequestHandler,
    NewOrderRequestHandler,
    AuthorizationRequestHandler,
    OrderFinalizationRequestHandler,
    ChallengeRequestHandler,
    OrderRequestHandler,
    CertRequestHandler,
)
from acmev2.handlers.base import ACMEModelResponse
from acmev2.handlers.handler import handle

from acmev2.services import (
    IDirectoryService,
    INonceService,
    IAccountService,
    IAuthorizationService,
    IOrderService,
    IChallengeService,
    ICertService,
)
from acmev2.services.services import ACMEEndpoint

from .test_services import (
    MemoryDirectoryService,
    MemoryNonceService,
    MemoryAccountService,
    MemoryAuthorizationService,
    MemoryOrderService,
    MemoryChallengeService,
    MemoryCertService,
)

from . import helpers
import logging

DEFAULT_RESOURCE_URL = "http://acme.localhost/acme/resource"

Message = TypedDict("Message", {"payload": str, "protected": str, "signature": str})
AcctId = str
OrdId = str
ResourceUrl = str
MessageBuilder = Callable[[Mapping[str, Any], josepy.JWKRSA, AcctId], Message]


def default_request_headers():
    return {"Content-Type": "application/jose+json"}


@pytest.fixture(autouse=True)
def setup():
    import dnsmock

    # I have no idea why these are necessary. If they don't exist then DNS resolution
    # will intermittently fail. Suspect it has something to do with Docker networking
    # and embedded DNS but it's not important enough to fix.
    dnsmock.bind_ip("acme.localhost", 443, "127.0.0.1")
    dnsmock.bind_ip("acme.localhost", 80, "127.0.0.1")
    from acmev2 import settings

    bindings = [
        (INonceService, MemoryNonceService()),
        (IDirectoryService, MemoryDirectoryService()),
        (IAccountService, MemoryAccountService()),
        (IOrderService, MemoryOrderService()),
        (IAuthorizationService, MemoryAuthorizationService()),
        (IChallengeService, MemoryChallengeService()),
        (ICertService, MemoryCertService()),
        (settings.ACMESettings, settings.ACMESettings()),
    ]
    inject.configure(
        lambda binder: [binder.bind(api, impl) for api, impl in bindings],
        bind_in_runtime=False,
        clear=True,
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    # handler.setFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger.addHandler(handler)


@pytest.fixture()
def private_key() -> rsa.RSAPrivateKey:
    return helpers.gen_private_key()


@pytest.fixture()
def jwk_rsa(private_key: rsa.RSAPrivateKey) -> josepy.JWK:
    return helpers.gen_jwk_rsa(private_key)


@pytest.fixture()
def message_builder(jwk_rsa: josepy.JWKRSA) -> MessageBuilder:
    default_jwk_rsa = jwk_rsa

    def builder(
        payload: Mapping[str, Any] = {},
        jwk_rsa: josepy.JWKRSA = None,
        acct_id: AcctId = None,
        url: str = None,
        nonce: str = None,
    ) -> Message:
        if not jwk_rsa:
            jwk_rsa = default_jwk_rsa

        nonce_service = inject.instance(INonceService)
        directory_service = inject.instance(IDirectoryService)

        header = {
            "alg": josepy.RS256.name,
            "nonce": nonce if nonce else nonce_service.generate(),
            "url": url or DEFAULT_RESOURCE_URL,
        }

        if acct_id:
            if "/" not in acct_id:
                acct_id = directory_service.url_for(ACMEEndpoint.account, acct_id)
            header["kid"] = acct_id
        else:
            header["jwk"] = jwk_rsa.public_key().to_json()

        def e(msg: dict):
            return josepy.encode_b64jose(json.dumps(msg).encode())

        msg: Message = {"protected": e(header), "payload": e(payload)}
        msg["signature"] = josepy.encode_b64jose(
            jwk_rsa.key.sign(
                f"{msg['protected']}.{msg['payload']}".encode(),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
        )

        return msg

    return builder


NewAccountRequest = Callable[[NewAccountRequestSchema], ACMEModelResponse]


@pytest.fixture
def new_account_request(
    message_builder: MessageBuilder,
) -> NewAccountRequest:
    def wrapped(msg: NewAccountRequestSchema) -> ACMEModelResponse:
        return handle(
            NewAccountRequestHandler(
                DEFAULT_RESOURCE_URL,
                "POST",
                msg=message_builder(msg.model_dump()),
                headers=default_request_headers(),
            )
        )

    return wrapped


NewOrderRequest = Callable[
    [NewOrderRequestSchema, AcctId, ResourceUrl], ACMEModelResponse
]


@pytest.fixture
def new_order_request(
    message_builder: MessageBuilder,
    default_account: AccountResource,
    default_order: OrderResource,
) -> NewOrderRequest:
    def wrapped(
        msg: NewOrderRequestSchema,
        acct_id: AcctId | None = None,
        url: ResourceUrl | None = None,
        request_url: str | None = None,
        headers: Mapping[str, str] = None,
        message_builder_kwargs={},
    ) -> ACMEModelResponse:
        if not url:
            url = "http://acme.localhost/acme/newOrder"

        if not request_url:
            request_url = url

        return handle(
            NewOrderRequestHandler(
                request_url,
                "POST",
                msg=message_builder(
                    msg.model_dump(),
                    acct_id=acct_id if acct_id else default_account.id,
                    url=url,
                    **message_builder_kwargs,
                ),
                headers=headers or default_request_headers(),
            )
        )

    return wrapped


OrderRequest = Callable[[EmptyMessageSchema, AcctId, ResourceUrl], ACMEModelResponse]


@pytest.fixture
def order_request(
    message_builder: MessageBuilder,
    default_account: AccountResource,
    default_order: OrderResource,
) -> OrderRequest:
    def wrapped(
        msg: EmptyMessageSchema,
        acct_id: AcctId | None = None,
        url: ResourceUrl | None = None,
        message_builder_kwargs={},
    ) -> ACMEModelResponse:
        return handle(
            OrderRequestHandler(
                (
                    url
                    if url
                    else inject.instance(IDirectoryService).url_for(
                        ACMEEndpoint.order, default_order.id
                    )
                ),
                "POST",
                msg=message_builder(
                    msg.model_dump(),
                    acct_id=acct_id if acct_id else default_account.id,
                    url=(
                        url
                        if url
                        else inject.instance(IDirectoryService).url_for(
                            ACMEEndpoint.order, default_order.id
                        )
                    ),
                    **message_builder_kwargs,
                ),
                headers=default_request_headers(),
            )
        )

    return wrapped


AuthorizationRequest = Callable[
    [EmptyMessageSchema, AcctId, ResourceUrl], ACMEModelResponse
]


@pytest.fixture
def authorization_request(
    message_builder: MessageBuilder,
    default_account: AccountResource,
    default_order: OrderResource,
) -> AuthorizationRequest:
    def wrapped(msg: AuthorizationSchema, **kwargs) -> ACMEModelResponse:
        if "acct_id" not in kwargs:
            kwargs["acct_id"] = default_account.id
        if "url" not in kwargs:
            kwargs["url"] = inject.instance(IDirectoryService).url_for(
                ACMEEndpoint.authz, default_order.authorizations[0].id
            )
        request_url = kwargs.pop("request_url", kwargs["url"])

        return handle(
            AuthorizationRequestHandler(
                request_url,
                "POST",
                msg=message_builder(msg.model_dump(), **kwargs),
                headers=default_request_headers(),
            )
        )

    return wrapped


ChallengeRequest = Callable[
    [EmptyMessageSchema, AcctId, ResourceUrl], ACMEModelResponse
]


@pytest.fixture
def chall_request(
    message_builder: MessageBuilder,
    default_account: AccountResource,
    default_order: OrderResource,
) -> AuthorizationRequest:
    def wrapped(msg: EmptyMessageSchema, **kwargs) -> ACMEModelResponse:
        if "acct_id" not in kwargs:
            kwargs["acct_id"] = default_account.id
        chall = default_order.authorizations[0].challenges[0]
        if "url" not in kwargs:
            directory_service = inject.instance(IDirectoryService)
            kwargs["url"] = directory_service.url_for(ACMEEndpoint.challenge, chall.id)
        request_url = kwargs.pop("request_url", kwargs["url"])

        return handle(
            ChallengeRequestHandler(
                request_url,
                "POST",
                msg=message_builder(msg.model_dump(), **kwargs),
                headers=default_request_headers(),
            )
        )

    return wrapped


FinalizeRequest = Callable[
    [OrderFinalizationRequestSchema, AcctId, ResourceUrl], ACMEModelResponse
]


@pytest.fixture
def finalize_order_request(
    message_builder: MessageBuilder,
    default_account: AccountResource,
    default_order: OrderResource,
) -> AuthorizationRequest:
    def wrapped(msg: OrderFinalizationRequestSchema, **kwargs) -> ACMEModelResponse:
        if "acct_id" not in kwargs:
            kwargs["acct_id"] = default_account.id

        if "url" not in kwargs:
            directory_service = inject.instance(IDirectoryService)
            kwargs["url"] = directory_service.url_for(
                ACMEEndpoint.finalize, default_order.id
            )
        request_url = kwargs.pop("request_url", kwargs["url"])
        headers = kwargs.pop("headers", default_request_headers())

        return handle(
            OrderFinalizationRequestHandler(
                request_url,
                "POST",
                msg=message_builder(msg.model_dump(), **kwargs),
                headers=headers,
            )
        )

    return wrapped


EABMessageBuilder = Callable[[str, str, josepy.JWKRSA], Message]


@pytest.fixture()
def eab_message_builder() -> EABMessageBuilder:
    def builder(kid: str, hmac_key: str, outerjwk: josepy.JWKRSA) -> Message:
        outerjwk_json = json.dumps(outerjwk.public_key().to_partial_json()).encode()

        eab = acme.jws.JWS.sign(
            outerjwk_json,
            josepy.jwk.JWKOct(key=josepy.decode_b64jose(hmac_key)),
            josepy.jwa.HS256,
            None,
            DEFAULT_RESOURCE_URL,
            kid,
        )

        return eab.to_partial_json()

    return builder


@pytest.fixture()
def default_account(setup, message_builder: MessageBuilder) -> AccountResource:
    response = handle(
        NewAccountRequestHandler(
            DEFAULT_RESOURCE_URL,
            "POST",
            msg=message_builder({"termsOfServiceAgreed": True}),
            headers=default_request_headers(),
        )
    )

    return response.msg


GenAccount = Callable[[], tuple[AccountResource, josepy.JWK]]


@pytest.fixture()
def gen_account(message_builder: MessageBuilder) -> GenAccount:
    def wrapped() -> tuple[AccountResource, josepy.JWK]:
        jwk_rsa = helpers.gen_jwk_rsa(helpers.gen_private_key())

        msg = message_builder(
            {
                "termsOfServiceAgreed": True,
            },
            jwk_rsa,
        )
        response = handle(
            NewAccountRequestHandler(
                DEFAULT_RESOURCE_URL, "POST", msg=msg, headers=default_request_headers()
            )
        )

        return response.msg, jwk_rsa

    return wrapped


@pytest.fixture()
def second_account(setup, gen_account) -> tuple[AccountResource, josepy.JWK]:
    return gen_account()


@pytest.fixture()
def default_order(
    setup, default_account, message_builder: MessageBuilder
) -> OrderResource:
    directory_service = inject.instance(IDirectoryService)
    new_order = message_builder(
        {
            "identifiers": [
                {"type": "dns", "value": "acme.localhost"},
                {"type": "dns", "value": "test2.acme"},
            ]
        },
        acct_id=default_account.id,
    )
    response = handle(
        NewOrderRequestHandler(
            DEFAULT_RESOURCE_URL,
            "POST",
            msg=new_order,
            headers=default_request_headers(),
        )
    )

    return response.msg


class LocalACMEAdapter(requests.adapters.HTTPAdapter):

    def req_by_path(self, path):
        import re

        if path.startswith("/acme/newnonce/"):
            return NewNonceRequestHandler
        elif path.startswith("/acme/newaccount/"):
            return NewAccountRequestHandler
        elif path.startswith("/acme/neworders/"):
            return NewOrderRequestHandler
        elif path.startswith("/acme/authz/"):
            return AuthorizationRequestHandler
        elif re.match(r"/acme/order/[a-zA-Z0-9]+/finalize", path):
            return OrderFinalizationRequestHandler
        elif path.startswith("/acme/chall/"):
            return ChallengeRequestHandler
        elif path.startswith("/acme/order/"):
            return OrderRequestHandler
        elif path.startswith("/acme/cert/"):
            return CertRequestHandler

        raise Exception("Message not found for path " + path)

    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    ):
        json_body = json.loads(request.body or "{}")
        req = self.req_by_path(request.path_url)(
            request.method, request.headers, json_body
        )
        resp: ACMEModelResponse = handle(req)

        if resp.msg:
            content = io.BytesIO(resp.serialize().encode())
        else:
            content = io.BytesIO()
        urllib_response = urllib3.HTTPResponse(
            content,
            resp.headers,
            resp.code,
            preload_content=False,
        )

        return self.build_response(
            request,
            urllib_response,
        )


@pytest.fixture
def acme_client(private_key: rsa.RSAPrivateKey):
    return gen_acme_client(private_key)


def gen_acme_client(rsa_key: rsa.RSAPrivateKey = None):
    directory = acme.client.messages.Directory.from_json(
        {
            "newAuthz": "http://acme.localhost/acme/new-authz/",
            "newNonce": "http://acme.localhost/acme/newnonce/",
            "newAccount": "http://acme.localhost/acme/newaccount/",
            "newOrder": "http://acme.localhost/acme/neworders/",
            "revokeCert": "http://acme.localhost/acme/revokecert/",
            "keyChange": "http://acme.localhost/acme/key-change/",
            "renewalInfo": "http://acme.localhost/acme/renewal-info/",
            "meta": {},
        }
    )
    if rsa_key is None:
        rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    account_key = josepy.JWKRSA(key=rsa_key)

    net = acme.client.ClientNetwork(account_key, user_agent="simple_acme_dns/v2")
    net.session.mount("http://acme.localhost/acme/", LocalACMEAdapter())
    net.session.mount("http://localhost/acme/", LocalACMEAdapter())
    return acme.client.ClientV2(directory, net=net)
