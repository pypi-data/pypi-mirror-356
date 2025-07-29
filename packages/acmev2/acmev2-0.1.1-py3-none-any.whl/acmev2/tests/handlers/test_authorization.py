from box import Box
import inject

from acmev2.models import (
    OrderResource,
    EmptyMessageSchema,
    AuthorizationSchema,
    AuthorizationStatus,
)
from acmev2.services import IAuthorizationService
from acmev2.settings import ACMESettings
from acmev2.tests.conftest import GenAccount, AuthorizationRequest
from acmev2.tests.helpers import authz_by_url, resp_has_error, validate_authz
from acmev2.tests.test_base import TestServicesMixin
from acmev2.tests.test_services import MemoryAuthorizationService


class TestAuthorizationRequest(TestServicesMixin):

    def test_post_as_get_authorization(
        self,
        authorization_request: AuthorizationRequest,
        default_order: OrderResource,
    ):
        response = authorization_request(EmptyMessageSchema())
        resource = Box(response.msg.model_dump())

        assert response.code == 200
        assert resource.status == "pending"
        assert resource.expires is not None

        assert resource.identifier.type == default_order.identifiers[0].type
        assert resource.identifier.value == default_order.identifiers[0].value
        assert len(resource.challenges) == 1
        assert resource.challenges[0].status == "pending"
        assert len(resource.challenges[0].token) > 0

    def test_not_found(
        self,
        authorization_request: AuthorizationRequest,
    ):
        response = authorization_request(EmptyMessageSchema(), url="no-resource-found")
        assert response.code == 404

    def test_unauthorized(
        self, authorization_request: AuthorizationRequest, gen_account: GenAccount
    ):
        second_account, second_account_jwk = gen_account()

        response = authorization_request(
            EmptyMessageSchema(), acct_id=second_account.id, jwk_rsa=second_account_jwk
        )

        assert response.code == 401

    def test_deactivate(
        self, default_order: OrderResource, authorization_request: AuthorizationRequest
    ):

        authz = default_order.authorizations[0]
        validate_authz(authz)

        response = authorization_request(
            AuthorizationSchema(status=AuthorizationStatus.deactivated)
        )
        resource = Box(response.msg.model_dump())
        assert resource.status == "deactivated"

    def test_bad_deactivation(self, authorization_request: AuthorizationRequest):
        response = authorization_request(
            AuthorizationSchema(status=AuthorizationStatus.deactivated)
        )

        assert resp_has_error(response, "urn:ietf:params:acme:error:malformed")

    def test_retry_after(self, authorization_request: AuthorizationRequest):
        settings = inject.instance(ACMESettings)
        settings.authorization_client_delay = 30

        response = authorization_request(EmptyMessageSchema())
        assert "Retry-After" in response.headers
        assert response.headers["Retry-After"] == settings.authorization_client_delay
