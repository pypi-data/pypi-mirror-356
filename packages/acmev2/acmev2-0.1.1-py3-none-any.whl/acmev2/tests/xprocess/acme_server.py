from time import sleep
from typing import Mapping
from cryptography.x509 import CertificateSigningRequest
from flask import Flask, Blueprint, jsonify, request, Response
import os
import inject
import parse
import datetime
import subprocess
import threading
from acmev2.models import ChallengeStatus, AuthorizationStatus, OrderStatus
from acmev2.models.challenge import ChallengeResource
from acmev2.models.order import OrderResource
from acmev2.handlers import handle as process_acme_request
from acmev2 import settings
from acmev2.handlers import ACMERequestHandler
from acmev2.handlers import (
    NewNonceRequestHandler,
    CertRequestHandler,
    OrderRequestHandler,
    NewOrderRequestHandler,
    ChallengeRequestHandler,
    NewAccountRequestHandler,
    AuthorizationRequestHandler,
    OrderFinalizationRequestHandler,
)
from acmev2.services.services import (
    ACMEEndpoint,
    INonceService,
    IDirectoryService,
    IAccountService,
    IOrderService,
    IAuthorizationService,
    IChallengeService,
    ICertService,
)
from acmev2.tests.test_services import (
    MemoryNonceService,
    MemoryAccountService,
    MemoryAuthorizationService,
    MemoryCertService,
    MemoryChallengeService,
    MemoryDirectoryService,
    MemoryOrderService,
)

DIR = os.path.dirname(__file__)

app = Flask(__name__)


class DirectoryService(IDirectoryService):
    root_url = "http://localhost:8080/acme"
    external_account_required = False


class ChallengeService(MemoryChallengeService):
    auth_service = inject.attr(IAuthorizationService)
    order_service = inject.attr(IOrderService)
    account_service = inject.attr(IAccountService)
    chall_service = inject.attr(IChallengeService)

    def queue_validation(self, chall: ChallengeResource) -> ChallengeResource:
        if chall.status == ChallengeStatus.processing:
            return chall

        super().queue_validation(chall)

        def _validate():
            sleep(1)
            authz = self.auth_service.get(chall.authz_id)
            order = self.order_service.get(authz.order_id)
            acct = self.account_service.get(order.account_id)
            # chall.status = ChallengeStatus.valid
            # authz.status = AuthorizationStatus.valid
            self.validate(acct.jwk, order, authz, chall)

            # self.chall_service.update_status(chall, ChallengeStatus.valid)
            # self.auth_service.update_status(authz, AuthorizationStatus.valid)

        threading.Thread(target=_validate).start()
        return chall


class OrderService(MemoryOrderService):
    def process_finalization(
        self, order: OrderResource, csr: CertificateSigningRequest
    ) -> OrderResource:
        order.status = OrderStatus.valid
        self.order_csrs[order.id] = csr
        return order


bindings = [
    (INonceService, MemoryNonceService()),
    (IDirectoryService, DirectoryService()),
    (IAccountService, MemoryAccountService()),
    (IOrderService, OrderService()),
    (IAuthorizationService, MemoryAuthorizationService()),
    (IChallengeService, ChallengeService()),
    (ICertService, MemoryCertService()),
    (settings.ACMESettings, settings.ACMESettings()),
]


inject.configure(
    lambda binder: [binder.bind(api, impl) for api, impl in bindings],
    bind_in_runtime=False,
    clear=True,
)


@app.route("/directory")
def directory():
    directory_service = inject.instance(IDirectoryService)
    return jsonify(directory_service.get_directory())


def translateACMERequest(ACMERequestType: ACMERequestHandler) -> Response:
    req = ACMERequestType(
        request.url,
        request.method,
        request.headers,
        request.json if request.is_json else None,
    )

    acme_resp = process_acme_request(req)
    resp_body = acme_resp.serialize() if acme_resp.msg else None
    resp = Response(
        resp_body,
        status=acme_resp.code,
        headers=acme_resp.headers,
    )

    return resp


@app.route("/acme/newNonce", methods=["HEAD", "GET"])
def newNonce():
    return translateACMERequest(NewNonceRequestHandler)


@app.route(
    "/acme/newAcct",
    methods=["POST"],
)
def newAccount():
    return translateACMERequest(NewAccountRequestHandler)


@app.route(
    "/acme/newOrder",
    methods=["POST"],
)
def newOrder():
    return translateACMERequest(NewOrderRequestHandler)


@app.route(
    "/acme/authz/<identifier>",
    methods=["POST"],
)
def authz(identifier):
    return translateACMERequest(AuthorizationRequestHandler)


@app.route(
    "/acme/chall/<identifier>",
    methods=["POST"],
)
def chall(identifier):
    return translateACMERequest(ChallengeRequestHandler)


@app.route(
    "/acme/order/<identifier>/finalize",
    methods=["POST"],
)
def finalize(identifier):
    return translateACMERequest(OrderFinalizationRequestHandler)


@app.route(
    "/acme/order/<identifier>",
    methods=["POST"],
)
def order(identifier):
    return translateACMERequest(OrderRequestHandler)


@app.route(
    "/acme/cert/<identifier>",
    methods=["POST"],
)
def cert(identifier):
    body = translateACMERequest(CertRequestHandler)
    return body


if __name__ == "__main__":
    inject.instance(IAccountService).hmacs["kid"] = "hmac"
    cert_path = "/tmp/acmev2.flask.crt"
    key_path = "/tmp/acmev2.flask.key"
    if not os.path.exists(key_path):
        subprocess.call(
            [
                "openssl",
                "req",
                "-new",
                "-newkey",
                "rsa:2048",
                "-days",
                "3650",
                "-nodes",
                "-x509",
                "-keyout",
                key_path,
                "-out",
                cert_path,
                "-subj",
                "/CN=acmeca.localhost",
                "-addext",
                "subjectAltName = DNS:acmeca.localhost",
            ]
        )

    app.run(
        debug=True, host="0.0.0.0", port=8080
    )  # , ssl_context=(cert_path, key_path))
