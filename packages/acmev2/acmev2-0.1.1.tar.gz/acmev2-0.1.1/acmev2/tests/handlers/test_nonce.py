import pytest
from acmev2.errors import ACMEMethodNotAllowedError
from acmev2.handlers import NewNonceRequestHandler
from acmev2.handlers.handler import handle
from acmev2.services import ACMEEndpoint
from acmev2.tests.helpers import resp_has_error
from acmev2.tests.test_base import TestServicesMixin
from acmev2.tests.conftest import default_request_headers
from acmev2.models import AccountResource, NewOrderRequestSchema, Identifier
from ..conftest import NewOrderRequest


class TestNonceRequest(TestServicesMixin):
    """
    https://datatracker.ietf.org/doc/html/rfc8555/#section-7.2
    Tests getting a new nonce.
    """

    def test_head(self):
        request = NewNonceRequestHandler(
            self.directory_service.url_for(ACMEEndpoint.newNonce),
            "HEAD",
            headers=default_request_headers(),
        )
        response = handle(request)

        nonce = response.headers.get("Replay-Nonce")
        assert nonce is not None
        assert len(nonce) > 0

        assert response.headers.get("Cache-Control") == "no-store"
        assert response.code == 200
        assert response.msg is None

        assert "Link" in response.headers

    def test_get(self):
        request = NewNonceRequestHandler(
            self.directory_service.url_for(ACMEEndpoint.newNonce),
            "GET",
            headers=default_request_headers(),
        )
        response = handle(request)

        nonce = response.headers.get("Replay-Nonce")
        assert nonce is not None
        assert len(nonce) > 0

        assert response.headers.get("Cache-Control") == "no-store"
        assert response.code == 204
        assert response.msg is None

    def test_invalid_verb(self):
        request = NewNonceRequestHandler(
            self.directory_service.url_for(ACMEEndpoint.newNonce),
            "POST",
            headers=default_request_headers(),
        )
        response = handle(request)
        assert resp_has_error(response, "urn:ietf:params:acme:error:malformed")

    def test_bad_nonce(self, new_order_request: NewOrderRequest):
        response = new_order_request(
            NewOrderRequestSchema(
                identifiers=[Identifier(type="dns", value="acme.localhost")]
            ),
            message_builder_kwargs={"nonce": "invalid"},
        )

        assert resp_has_error(response, "urn:ietf:params:acme:error:badNonce")
        assert response.code == 400
