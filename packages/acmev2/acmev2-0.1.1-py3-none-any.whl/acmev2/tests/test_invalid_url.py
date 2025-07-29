from acmev2.models import AccountResource, AccountStatus
from acmev2.handlers import ACMEModelResponse
from acmev2.models import Identifier, NewOrderRequestSchema

from acmev2.tests.conftest import NewOrderRequest
from acmev2.tests.helpers import resp_has_error


class TestInvalidUrl:
    def test_invalid_url(self, new_order_request: NewOrderRequest):

        resp = new_order_request(
            NewOrderRequestSchema(
                identifiers=[Identifier(type="dns", value="acme.localhost")]
            )
        )

        assert resp.code == 201

        resp = new_order_request(
            NewOrderRequestSchema(
                identifiers=[Identifier(type="dns", value="acme.localhost")]
            ),
            request_url="https://invalid.localhost/acme/newOrder",
        )

        assert resp_has_error(resp, "urn:ietf:params:acme:error:unauthorized")
