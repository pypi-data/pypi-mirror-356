import inject
from acmev2.models import EmptyMessageSchema
from acmev2.services import IDirectoryService
from acmev2.services.services import ACMEEndpoint
from acmev2.tests.conftest import OrderRequest
from acmev2.tests.helpers import resp_has_error


class TestOrder:

    def test_order_post_as_get_contains_location(self, order_request: OrderRequest):
        # All order post-as-get needs to have the 'Location' header. Why? Who knows.
        response = order_request(EmptyMessageSchema())
        assert "Location" in response.headers
        assert response.msg.id is not None

    def test_invalid_account(self, order_request: OrderRequest, gen_account):
        acct, jwk = gen_account()
        response = order_request(
            EmptyMessageSchema(),
            acct_id=acct.id,
            message_builder_kwargs={"jwk_rsa": jwk},
        )

        assert resp_has_error(response, "urn:ietf:params:acme:error:unauthorized")

    def test_account_not_found(self, order_request: OrderRequest):
        url = inject.instance(IDirectoryService).url_for(
            ACMEEndpoint.order, "invalid-id"
        )
        response = order_request(EmptyMessageSchema(), url=url)

        assert response.code == 404
        assert resp_has_error(response, "resourceNotFound")
