from acmev2.models import AccountResource, AccountStatus
from acmev2.handlers import ACMEModelResponse
from acmev2.models import Identifier, NewOrderRequestSchema

from acmev2.tests.conftest import NewOrderRequest
from acmev2.tests.helpers import resp_has_error


class TestInvalidContentType:
    def test_invalid_content_type(self, new_order_request: NewOrderRequest):
        resp = new_order_request(
            NewOrderRequestSchema(
                identifiers=[Identifier(type="dns", value="acme.localhost")]
            )
        )

        assert resp.code == 201

        resp: ACMEModelResponse = new_order_request(
            NewOrderRequestSchema(
                identifiers=[Identifier(type="dns", value="acme.localhost")]
            ),
            request_url="https://invalid.localhost/acme/newOrder",
            headers={"Content-Type": "wrong-type"},
        )

        assert resp.code == 415
        assert resp_has_error(resp, "urn:ietf:params:acme:error:malformed")
