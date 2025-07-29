from datetime import datetime, timedelta

import inject
import pytest

from acmev2.handlers import ACMEModelResponse
from acmev2.models import (
    AccountResource,
    AccountStatus,
    Identifier,
    NewOrderRequestSchema,
    OrderResource,
    OrderStatus,
    AuthorizationStatus,
)
from acmev2.services import ACMEEndpoint, IDirectoryService, IOrderService
from acmev2.tests.conftest import NewOrderRequest
from acmev2.tests.helpers import resp_has_error


class TestInvalidAccount:
    @pytest.fixture
    def order_generator(self, new_order_request: NewOrderRequest):
        directory_service = inject.instance(IDirectoryService)
        order_service = inject.instance(IOrderService)

        def wrapped(domains: list[str]):
            response = new_order_request(
                NewOrderRequestSchema(
                    identifiers=[Identifier(type="dns", value=d) for d in domains]
                )
            )
            finalize = response.msg.model_dump()["finalize"]
            ord_id = directory_service.identifier_from_url(
                ACMEEndpoint.finalize, finalize
            )
            return order_service.get(ord_id)

        return wrapped

    def test_expired_order(self, order_generator):
        order_service = inject.instance(IOrderService)
        ord: OrderResource = order_generator(["acme.localhost"])
        ord.expires = datetime.now() - timedelta(minutes=5)
        ord = order_service.resolve_state(ord)

        assert ord.status == OrderStatus.invalid

    def test_expired_authz(self, order_generator):
        order_service = inject.instance(IOrderService)
        ord: OrderResource = order_generator(["acme.localhost"])
        ord.authorizations[0].expires = datetime.now() - timedelta(minutes=5)
        ord = order_service.resolve_state(ord)

        assert ord.status == OrderStatus.invalid
        assert ord.authorizations[0].status == AuthorizationStatus.expired

    def test_do_not_transition_valid_order(self, order_generator):
        order_service = inject.instance(IOrderService)
        ord: OrderResource = order_generator(["acme.localhost"])
        ord.status = OrderStatus.valid
        ord.authorizations[0].expires = datetime.now() - timedelta(minutes=5)
        ord = order_service.resolve_state(ord)

        assert ord.status == OrderStatus.valid

    def test_order_ready(self, order_generator):
        order_service = inject.instance(IOrderService)
        ord: OrderResource = order_generator(["acme.localhost"])

        ord.authorizations[0].status = AuthorizationStatus.valid
        ord = order_service.resolve_state(ord)

        assert ord.status == OrderStatus.ready

    def test_do_not_transition_terminal_authz(self, order_generator):
        order_service = inject.instance(IOrderService)
        ord: OrderResource = order_generator(["acme.localhost"])
        ord.authorizations[0].status = AuthorizationStatus.deactivated
        ord = order_service.resolve_state(ord)

        assert ord.status == OrderStatus.invalid
        assert ord.authorizations[0].status == AuthorizationStatus.deactivated
