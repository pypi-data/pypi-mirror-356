import inject
import josepy.b64
import pytest
from acmev2.errors import ACMEBadCSRDetail
from acmev2.models import AccountResource, OrderResource, OrderStatus
from acmev2.models.authorization import AuthorizationStatus
from acmev2.handlers import (
    NewAccountRequestHandler,
    NewOrderRequestHandler,
    CertRequestHandler,
    handle,
    OrderFinalizationRequestHandler,
)
from cryptography.hazmat.primitives import serialization
from acmev2.handlers.base import ACMEModelResponse
from acmev2.services import IDirectoryService, ACMEEndpoint
from acmev2.tests.conftest import MessageBuilder, default_request_headers
from acmev2.tests.helpers import (
    authz_by_url,
    chall_by_url,
    gen_csr,
    gen_jwk_rsa,
    gen_private_key,
    resp_has_error,
    make_order_ready,
)
from box import Box
import josepy.jwk
import josepy
from datetime import datetime, timedelta
from cryptography import x509


class TestCertRequest:

    def test_cert_ready(
        self,
        private_key: josepy.jwk.JWK,
        default_order: OrderResource,
        default_account: AccountResource,
        message_builder: MessageBuilder,
    ):
        directory_service = inject.instance(IDirectoryService)
        make_order_ready(default_order)
        order_request = message_builder(
            {
                "csr": josepy.encode_b64jose(
                    gen_csr(
                        private_key,
                        default_order.identifiers[0].value,
                        [default_order.identifiers[0].value]
                        + [i.value for i in default_order.identifiers],
                    ).public_bytes(serialization.Encoding.DER)
                )
            },
            acct_id=default_account.id,
            url=directory_service.url_for(ACMEEndpoint.finalize, default_order.id),
        )

        handle(
            OrderFinalizationRequestHandler(
                directory_service.url_for(ACMEEndpoint.finalize, default_order.id),
                "POST",
                msg=order_request,
                headers=default_request_headers(),
            )
        )
        cert = handle(
            CertRequestHandler(
                directory_service.url_for(ACMEEndpoint.cert, default_order.id),
                "POST",
                msg=message_builder(
                    acct_id=default_account.id,
                    url=directory_service.url_for(ACMEEndpoint.cert, default_order.id),
                ),
                headers=default_request_headers(),
            )
        )
        assert cert.code == 200
        certs = x509.load_pem_x509_certificates(cert.serialize().encode())
        assert len(certs) == 2
        assert (
            certs[0].subject.rfc4514_string()
            == f"CN={default_order.identifiers[0].value}"
        )

    def test_cert_not_found(
        self,
        default_order: OrderResource,
        default_account: AccountResource,
        message_builder: MessageBuilder,
    ):
        directory_service = inject.instance(IDirectoryService)
        cert = handle(
            CertRequestHandler(
                directory_service.url_for(ACMEEndpoint.cert, default_order.id),
                "POST",
                msg=message_builder(
                    acct_id=default_account.id,
                    url=directory_service.url_for(ACMEEndpoint.cert, default_order.id),
                ),
                headers=default_request_headers(),
            )
        )
        assert cert.code == 404
