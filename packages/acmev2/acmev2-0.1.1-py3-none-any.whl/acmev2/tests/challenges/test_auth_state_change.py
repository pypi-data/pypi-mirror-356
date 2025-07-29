import inject
import pytest
from acmev2.challenges import CustomChallengeValidator
from acmev2.challenges.base import ChallengeValidator
from acmev2.handlers import ACMEModelResponse
from acmev2.models import (
    NewOrderRequestSchema,
    Identifier,
    ChallengeType,
    AccountResource,
    OrderResource,
    AuthorizationStatus,
    OrderStatus,
    EmptyMessageSchema,
)
from acmev2.settings import ACMESettings, Challenges
from acmev2.tests.conftest import NewOrderRequest, OrderRequest
from acmev2.tests.helpers import authz_by_url
from acmev2.services import (
    IChallengeService,
    IAuthorizationService,
    IOrderService,
    IDirectoryService,
    ACMEEndpoint,
)
from box import Box


class TestAuthStateChange:

    @pytest.fixture()
    def passing_custom_validator(self, setup):
        class AlwaysTrueCustomChallengeValidator(CustomChallengeValidator):
            def validate(self, challenge_validator: ChallengeValidator) -> bool:
                return True

        inject.get_injector()._bindings[
            CustomChallengeValidator
        ] = lambda: AlwaysTrueCustomChallengeValidator()

    @pytest.fixture()
    def failing_custom_validator(self, setup):
        class AlwaysFalseCustomChallengeValidator(CustomChallengeValidator):
            def validate(self, challenge_validator: ChallengeValidator) -> bool:
                return False

        inject.get_injector()._bindings[
            CustomChallengeValidator
        ] = lambda: AlwaysFalseCustomChallengeValidator()

    def test_chall_makes_auth_valid(
        self,
        default_account: AccountResource,
        new_order_request: NewOrderRequest,
        order_request: OrderRequest,
        passing_custom_validator,
    ):
        settings = inject.instance(ACMESettings)
        directory_service = inject.instance(IDirectoryService)
        chall_service = inject.instance(IChallengeService)
        authz_service = inject.instance(IAuthorizationService)
        order_service = inject.instance(IOrderService)
        settings.challenges_available = [Challenges.custom, Challenges.http_01]
        domains = ["domain1.acme.locahost", "domain2.acme.localhost"]
        response: ACMEModelResponse = new_order_request(
            NewOrderRequestSchema(
                identifiers=[Identifier(type="dns", value=domain) for domain in domains]
            )
        )

        resource = Box(response.msg.model_dump())
        assert len(resource.identifiers) == 2
        ord_id = directory_service.identifier_from_url(
            ACMEEndpoint.finalize, resource.finalize
        )

        for authz_url in resource.authorizations:
            authz = authz_by_url(authz_url)
            assert len(authz.challenges) == len(settings.challenges_available)
            for chall in authz.challenges:
                if chall.type == ChallengeType.custom:
                    chall_service.validate(
                        default_account.jwk, order_service.get(ord_id), authz, chall
                    )

            assert authz_service.get(authz.id).status == AuthorizationStatus.valid

        order = order_service.get(ord_id)
        assert order.status == OrderStatus.ready

    @pytest.mark.slow
    def test_chall_makes_auth_invalid(
        self,
        default_account: AccountResource,
        new_order_request: NewOrderRequest,
        order_request: OrderRequest,
        failing_custom_validator,
    ):
        settings = inject.instance(ACMESettings)
        directory_service = inject.instance(IDirectoryService)
        chall_service = inject.instance(IChallengeService)
        authz_service = inject.instance(IAuthorizationService)
        order_service = inject.instance(IOrderService)
        settings.challenges_available = [Challenges.custom, Challenges.http_01]
        domains = ["domain1.acme.locahost", "domain2.acme.localhost"]
        response: ACMEModelResponse = new_order_request(
            NewOrderRequestSchema(
                identifiers=[Identifier(type="dns", value=domain) for domain in domains]
            )
        )

        resource = Box(response.msg.model_dump())
        assert len(resource.identifiers) == 2
        ord_id = directory_service.identifier_from_url(
            ACMEEndpoint.finalize, resource.finalize
        )

        for authz_url in resource.authorizations:
            authz = authz_by_url(authz_url)
            assert len(authz.challenges) == len(settings.challenges_available)
            for chall in authz.challenges:
                if chall.type == ChallengeType.custom:
                    chall_service.validate(
                        default_account.jwk, order_service.get(ord_id), authz, chall
                    )

            assert authz_service.get(authz.id).status == AuthorizationStatus.pending

        order = order_service.get(ord_id)
        assert order.status != OrderStatus.ready
