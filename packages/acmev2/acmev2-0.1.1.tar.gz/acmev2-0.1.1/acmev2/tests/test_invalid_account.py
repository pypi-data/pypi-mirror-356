from acmev2.models import AccountResource, AccountStatus
from acmev2.handlers import ACMEModelResponse
from acmev2.models import Identifier, NewOrderRequestSchema

from acmev2.tests.conftest import NewOrderRequest
from acmev2.tests.helpers import resp_has_error


class TestInvalidAccount:
    def test_deactivated_account(
        self, new_order_request: NewOrderRequest, default_account: AccountResource
    ):
        def make_request() -> ACMEModelResponse:
            return new_order_request(
                NewOrderRequestSchema(
                    identifiers=[Identifier(type="dns", value="acme.localhost")]
                )
            )

        resp = make_request()
        assert resp.code == 201

        default_account.status = AccountStatus.deactivated
        resp = make_request()
        assert resp_has_error(resp, "urn:ietf:params:acme:error:malformed")

    def test_revoked_account(
        self,
        default_account: AccountResource,
        new_order_request: NewOrderRequest,
    ):
        def make_request() -> ACMEModelResponse:
            return new_order_request(
                NewOrderRequestSchema(
                    identifiers=[Identifier(type="dns", value="acme.localhost")]
                )
            )

        resp = make_request()
        assert resp.code == 201

        default_account.status = AccountStatus.revoked
        resp = make_request()
        assert resp_has_error(resp, "urn:ietf:params:acme:error:malformed")
