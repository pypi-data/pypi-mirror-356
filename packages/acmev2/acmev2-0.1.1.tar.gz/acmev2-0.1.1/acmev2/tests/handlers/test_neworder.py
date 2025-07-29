import inject
from pydantic import ValidationError
import pytest
from acmev2.settings import ACMESettings
from acmev2.models import AccountResource, NewOrderRequestSchema, Identifier
from acmev2.handlers import NewOrderRequestHandler, handle
from acmev2.tests.conftest import MessageBuilder
from acmev2.tests.helpers import resp_has_error
from box import Box

from acmev2.tests.test_base import TestServicesMixin
from ..conftest import NewOrderRequest


class TestNewOrderRequest(TestServicesMixin):

    def test_invalid_wildcard(self, new_order_request: NewOrderRequest):
        response = new_order_request(
            NewOrderRequestSchema(
                identifiers=[Identifier(type="dns", value="*.acme.localhost")]
            )
        )

        assert resp_has_error(response, "urn:ietf:params:acme:error:rejectedIdentifier")

    def test_invalid_identifier_type(self, new_order_request: NewOrderRequest):
        with pytest.raises(ValidationError):
            new_order_request(
                NewOrderRequestSchema(
                    identifiers=[Identifier(type="invalid", value="acme.localhost")]
                )
            )

    def test_too_many_identifiers(self, new_order_request: NewOrderRequest):
        self.settings.max_identifiers = 5

        def build_message():
            return new_order_request(
                NewOrderRequestSchema(
                    identifiers=[
                        Identifier(type="dns", value=f"{idx}.acme.localhost")
                        for idx in range(20)
                    ]
                )
            )

        response = build_message()
        assert resp_has_error(response, "urn:ietf:params:acme:error:malformed")

        self.settings.max_identifiers = 100
        response = build_message()
        assert response.code == 201

    def test_no_identifiers(self, new_order_request: NewOrderRequest):
        response = new_order_request(NewOrderRequestSchema(identifiers=[]))
        assert resp_has_error(response, "urn:ietf:params:acme:error:malformed")

    def test_order_created(self, new_order_request: NewOrderRequest):
        response = new_order_request(
            NewOrderRequestSchema(
                identifiers=[Identifier(type="dns", value="acme.localhost")]
            )
        )

        assert "Location" in response.headers
        assert response.code == 201
        resource = Box(response.msg.model_dump())

        assert len(resource["identifiers"]) == 1
        assert resource.finalize is not None
        # some clients require this even though it's optional!
        assert "certificate" in resource
        assert resource.status == "pending"

    def test_blacklisted_domains(self, new_order_request: NewOrderRequest):
        settings = inject.instance(ACMESettings)

        def make_request(domains: list[str]):
            return new_order_request(
                NewOrderRequestSchema(
                    identifiers=[
                        Identifier(type="dns", value=domain) for domain in domains
                    ]
                )
            )

        domain_test_cases = [
            ([r".*?\.invalid\.acme"], ["domain.invalid.acme"]),
            ([r".*?\.invalid\.acme"], ["domain.valid.acme", "domain.invalid.acme"]),
            # Testing the nth rule is evaluated, not just the first
            (
                [r".*?\.unused\.acme", r".*?\.invalid\.acme"],
                ["domain.valid.acme", "d.invalid.acme"],
            ),
            # must end with .acme
            ([r".*(?<!(\.acme))$"], ["invalid.com"]),
            ([r".*(?<!(\.acme))$"], ["invalid.com"]),
            # must not be subdomain.protected.acme or protected.acme
            ([r"^(.*\.)?protected.acme"], ["error.protected.acme"]),
            ([r"^(.*\.)?protected.acme"], ["protected.acme"]),
        ]

        for blacklist, domains in domain_test_cases:
            # reset blacklist
            settings.blacklisted_domains = []
            # first request should succeed
            assert make_request(domains).code == 201
            # set blacklist
            settings.blacklisted_domains = blacklist
            # second request should fail
            assert resp_has_error(
                make_request(domains),
                "urn:ietf:params:acme:error:rejectedIdentifier",
            ), {"blacklist": blacklist, "domains": domains}

    def test_unauthorized(self, new_order_request: NewOrderRequest):
        response = new_order_request(
            NewOrderRequestSchema(
                identifiers=[Identifier(type="dns", value="acme.localhost")]
            ),
            "invalid-acct-id",
        )

        assert resp_has_error(
            response, "urn:ietf:params:acme:error:accountDoesNotExist"
        )
