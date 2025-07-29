import inject
import josepy.b64
from acmev2.errors import ACMEBadCSRDetail
from acmev2.models import AccountResource, OrderResource, OrderStatus
from acmev2.handlers import (
    handle,
    OrderFinalizationRequestHandler,
)
from cryptography.hazmat.primitives import serialization
from acmev2.handlers.base import ACMEModelResponse
from acmev2.models.order import OrderFinalizationRequestSchema
from acmev2.services import IDirectoryService, ACMEEndpoint
from acmev2.settings import ACMESettings
from acmev2.tests.conftest import MessageBuilder
from acmev2.tests.helpers import (
    gen_csr,
    gen_encoded_csr,
    resp_has_error,
    make_order_ready,
)
from box import Box
import josepy.jwk
import josepy
from datetime import datetime, timedelta
from ..conftest import default_request_headers


class TestFinalizeRequest:

    def test_finalize_ready(
        self,
        finalize_order_request,
        private_key: josepy.jwk.JWK,
        default_order: OrderResource,
    ):
        make_order_ready(default_order)

        assert default_order.status == "ready"

        response: ACMEModelResponse = finalize_order_request(
            OrderFinalizationRequestSchema(
                csr=gen_encoded_csr(
                    private_key,
                    order=default_order,
                )
            )
        )

        resource = Box(response.msg.model_dump())

        assert response.code == 200
        assert resource.status == "processing"
        assert resource.expires is not None
        assert len(resource.identifiers) == len(default_order.identifiers)
        assert len(resource.authorizations) == len(default_order.authorizations)
        assert "finalize" not in resource
        assert "certificate" not in resource

    def test_misbehaving_ua_finalize(
        self,
        finalize_order_request,
        private_key: josepy.jwk.JWK,
        default_order: OrderResource,
    ):
        # Addresses issue https://github.com/cert-manager/cert-manager/issues/5062
        settings = inject.instance(ACMESettings)

        settings.mask_order_processing_status_ua_match = "^testagent.*"
        make_order_ready(default_order)

        assert default_order.status == "ready"

        headers = default_request_headers()
        headers["User-Agent"] = "testagent/0.0.1"
        response: ACMEModelResponse = finalize_order_request(
            OrderFinalizationRequestSchema(
                csr=gen_encoded_csr(
                    private_key,
                    order=default_order,
                )
            ),
            headers=headers,
        )

        resource = Box(response.msg.model_dump())

        assert response.code == 200
        assert resource.status == "pending"
        assert resource.expires is not None
        assert len(resource.identifiers) == len(default_order.identifiers)
        assert len(resource.authorizations) == len(default_order.authorizations)
        assert "finalize" not in resource
        assert "certificate" not in resource

    def test_authorization_validation_errors(
        self,
        finalize_order_request,
        private_key: josepy.jwk.JWK,
        default_order: OrderResource,
    ):
        default_order.status = OrderStatus.ready

        response: ACMEModelResponse = finalize_order_request(
            OrderFinalizationRequestSchema(
                csr=gen_encoded_csr(
                    private_key,
                    order=default_order,
                )
            )
        )

        assert resp_has_error(
            response,
            "urn:ietf:params:acme:error:badCSR",
            str(ACMEBadCSRDetail.orderNotAuthorized),
        )

    def test_csr_validation_errors(
        self,
        finalize_order_request,
        private_key: josepy.jwk.JWK,
        default_order: OrderResource,
    ):
        make_order_ready(default_order)

        def request(cn: str = None, sans: list[str] = None):
            if cn is None:
                cn = default_order.identifiers[0].value
            if sans is None:
                sans = [default_order.identifiers[0].value]

            return finalize_order_request(
                OrderFinalizationRequestSchema(
                    csr=gen_encoded_csr(private_key, cn, sans)
                )
            )

        requests: tuple[ACMEBadCSRDetail, ACMEModelResponse] = (
            # CN doesn't match SANS and isn't in identifiers
            (ACMEBadCSRDetail.cnMissingFromSan, request(cn="extracn.localhost")),
            # SANS has an extra item that isn't in the identifiers
            (
                ACMEBadCSRDetail.csrOrderMismatch,
                request(sans=[default_order.identifiers[0].value, "invalid.localhost"]),
            ),
            # Order isn't authorized for CN domains
            (
                ACMEBadCSRDetail.csrOrderMismatch,
                request(
                    cn="extracn.localhost",
                    sans=[default_order.identifiers[0].value, "extracn.localhost"],
                ),
            ),
            # SANS can't be empty
            (ACMEBadCSRDetail.sansRequired, request(sans=[])),
        )

        for idx, (err_detail, resp) in enumerate(requests):
            assert resp_has_error(
                resp, "urn:ietf:params:acme:error:badCSR", str(err_detail)
            ), f"Error running test {idx+1}"

    def test_expired_order(
        self,
        finalize_order_request,
        default_order: OrderResource,
        private_key,
    ):
        default_order.expires = datetime.now() - timedelta(hours=1)
        make_order_ready(default_order)
        response: ACMEModelResponse = finalize_order_request(
            OrderFinalizationRequestSchema(
                csr=gen_encoded_csr(
                    private_key,
                    order=default_order,
                )
            )
        )

        assert resp_has_error(response, "urn:ietf:params:acme:error:orderNotReady")

    def test_unauthorized(
        self,
        default_order,
        finalize_order_request,
        second_account,
        private_key: josepy.jwk.JWK,
    ):
        second_account, second_account_jwk = second_account

        response: ACMEModelResponse = finalize_order_request(
            OrderFinalizationRequestSchema(
                csr=gen_encoded_csr(
                    private_key,
                    order=default_order,
                )
            ),
            acct_id=second_account.id,
            jwk_rsa=second_account_jwk,
        )

        assert resp_has_error(response, "urn:ietf:params:acme:error:unauthorized")

    def test_not_found(
        self,
        default_order,
        finalize_order_request,
        private_key: josepy.jwk.JWK,
    ):
        directory_service = inject.instance(IDirectoryService)

        response: ACMEModelResponse = finalize_order_request(
            OrderFinalizationRequestSchema(
                csr=gen_encoded_csr(
                    private_key,
                    order=default_order,
                )
            ),
            url=directory_service.url_for(
                ACMEEndpoint.finalize, default_order.id + "x"
            ),
        )

        assert resp_has_error(response, "resourceNotFound")
