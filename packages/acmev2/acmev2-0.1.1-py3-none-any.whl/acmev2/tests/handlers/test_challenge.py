import inject
from acmev2.handlers.base import ACMEModelResponse
from acmev2.models import AccountResource, OrderResource
from acmev2.handlers import (
    handle,
    ChallengeRequestHandler,
)
from acmev2.models.base import EmptyMessageSchema
from acmev2.services import IDirectoryService, ACMEEndpoint
from acmev2.tests.conftest import ChallengeRequest, MessageBuilder
from acmev2.tests.helpers import (
    authz_by_url,
    resp_has_error,
)
from box import Box
import josepy.jwk
from datetime import datetime, timedelta


class TestChallengeRequest:

    def test_begin_challenge_verification(
        self, default_order: OrderResource, chall_request: ChallengeRequest
    ):
        response: ACMEModelResponse = chall_request(EmptyMessageSchema())
        resource = Box(response.msg.model_dump())
        directory_service = inject.instance(IDirectoryService)
        assert (
            directory_service.url_for(
                ACMEEndpoint.authz, default_order.authorizations[0].id
            )
            in response.headers["Link"]
        )
        assert response.code == 200
        assert resource.status == "processing"
        assert resource.type == "http-01"
        assert len(resource.token) > 1
        assert resource.url is not None

    def test_expired_authz(
        self, default_order: OrderResource, chall_request: ChallengeRequest
    ):
        authz_resource = default_order.authorizations[0]
        authz_resource.expires = datetime.now() - timedelta(hours=1)
        response: ACMEModelResponse = chall_request(EmptyMessageSchema())
        assert resp_has_error(response, "urn:ietf:params:acme:error:malformed")

    def test_not_found(self, chall_request: ChallengeRequest):
        response: ACMEModelResponse = chall_request(EmptyMessageSchema(), url="invalid")
        assert response.code == 404

    def test_unauthorized(
        self,
        second_account: tuple[AccountResource, josepy.jwk.JWK],
        chall_request: ChallengeRequest,
    ):
        second_account, second_account_jwk = second_account
        response: ACMEModelResponse = chall_request(
            EmptyMessageSchema(), acct_id=second_account.id, jwk_rsa=second_account_jwk
        )
        assert response.code == 401
