import inject
import josepy.jwk

from acmev2.handlers import NewAccountRequestHandler, handle
from acmev2.models.account import AccountResource, NewAccountRequestSchema
from acmev2.services import IAccountService
from acmev2.settings import ACMESettings
from acmev2.tests.conftest import EABMessageBuilder, NewAccountRequest, MessageBuilder
from acmev2.tests.test_services import MemoryAccountService

from ..helpers import (
    gen_jwk_rsa,
    gen_private_key,
    resp_has_error,
)


class TestNewAccountRequest:

    def test_success(self, new_account_request: NewAccountRequest):
        account_service: MemoryAccountService = inject.instance(IAccountService)
        accounts = len(account_service.accounts)

        response = new_account_request(
            NewAccountRequestSchema(termsOfServiceAgreed=True)
        )
        assert len(account_service.accounts) == accounts + 1
        assert response.code == 201
        assert "Location" in response.headers

    def test_force_tos(self, new_account_request: NewAccountRequest):
        # Messages to the new account endpoint fail without
        # agreeing to the ToS
        response = new_account_request(NewAccountRequestSchema())
        assert resp_has_error(response, "urn:ietf:params:acme:error:userActionRequired")

    def test_invalid_contacts(self, new_account_request: NewAccountRequest):
        # Only support mailto: contacts per rfc6068. We don't get too carried
        # away trying to implement the whole ridiculous spec.
        response = new_account_request(
            NewAccountRequestSchema(
                termsOfServiceAgreed=True, contact=["mailto: invalid"]
            )
        )
        assert resp_has_error(response, "urn:ietf:params:acme:error:unsupportedContact")

    def test_only_return_existing_error(self, new_account_request: NewAccountRequest):
        # Only return existing errors if an account does not exist with the passed in jwk
        response = new_account_request(
            NewAccountRequestSchema(termsOfServiceAgreed=True, onlyReturnExisting=True)
        )
        assert resp_has_error(
            response, "urn:ietf:params:acme:error:accountDoesNotExist"
        )

    def test_lookup(self, new_account_request: NewAccountRequest):
        account_service: MemoryAccountService = inject.instance(IAccountService)
        accounts = len(account_service.accounts)

        new_account_request(NewAccountRequestSchema(termsOfServiceAgreed=True))
        lookup_response = new_account_request(
            NewAccountRequestSchema(termsOfServiceAgreed=True)
        )

        assert len(account_service.accounts) == accounts + 1
        assert lookup_response.code == 200
        assert "Location" in lookup_response.headers

    def test_eab_success(
        self,
        jwk_rsa: josepy.JWKRSA,
        new_account_request: NewAccountRequest,
        eab_message_builder: EABMessageBuilder,
    ):
        account_service: MemoryAccountService = inject.instance(IAccountService)
        kid, hmac_key = account_service.gen_hmac()

        response = new_account_request(
            NewAccountRequestSchema(
                termsOfServiceAgreed=True,
                externalAccountBinding=eab_message_builder(kid, hmac_key, jwk_rsa),
            )
        )

        assert response.code == 201
        msg: AccountResource = response.msg
        assert msg.id == account_service.bound_accounts[kid]

    def test_eab_already_bound(
        self,
        new_account_request: NewAccountRequest,
        eab_message_builder: EABMessageBuilder,
    ):
        account_service: MemoryAccountService = inject.instance(IAccountService)
        kid, hmac_key = account_service.gen_hmac()

        def make_request():
            jwk_rsa = gen_jwk_rsa(gen_private_key())

            return new_account_request(
                NewAccountRequestSchema(
                    termsOfServiceAgreed=True,
                    externalAccountBinding=eab_message_builder(kid, hmac_key, jwk_rsa),
                )
            )

        make_request()
        response = make_request()
        assert resp_has_error(response, "urn:ietf:params:acme:error:malformed")

    def test_eab_required(
        self,
        new_account_request: NewAccountRequest,
    ):
        settings = inject.instance(ACMESettings)

        settings.eab_required = True
        response = new_account_request(
            NewAccountRequestSchema(termsOfServiceAgreed=True)
        )

        assert resp_has_error(
            response, "urn:ietf:params:acme:error:externalAccountRequired"
        )

    def test_invalid_eab_kid(
        self,
        jwk_rsa: josepy.JWKRSA,
        new_account_request: NewAccountRequest,
        eab_message_builder: EABMessageBuilder,
    ):
        account_service: MemoryAccountService = inject.instance(IAccountService)
        _, hmac_key = account_service.gen_hmac()

        response = new_account_request(
            NewAccountRequestSchema(
                termsOfServiceAgreed=True,
                externalAccountBinding=eab_message_builder(
                    "invalid-kid", hmac_key, jwk_rsa
                ),
            )
        )

        assert resp_has_error(response, "urn:ietf:params:acme:error:malformed")

    def test_invalid_eab_hmac(
        self,
        jwk_rsa: josepy.JWKRSA,
        new_account_request: NewAccountRequest,
        eab_message_builder: EABMessageBuilder,
    ):
        account_service: MemoryAccountService = inject.instance(IAccountService)
        kid, _ = account_service.gen_hmac()

        response = new_account_request(
            NewAccountRequestSchema(
                termsOfServiceAgreed=True,
                externalAccountBinding=eab_message_builder(
                    kid, "invalid-hmac", jwk_rsa
                ),
            )
        )

        assert resp_has_error(response, "urn:ietf:params:acme:error:malformed")
