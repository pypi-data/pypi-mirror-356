import abc
import random
import string
from enum import Enum
from typing import Any, Mapping

import inject
import josepy.jwk
import parse
from cryptography.x509 import CertificateSigningRequest

import acmev2.models as models
from acmev2.models import (
    CertResource,
    AuthorizationStatus,
    ChallengeStatus,
    OrderStatus,
)
from acmev2 import challenges
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ACMEResourceType(str, Enum):
    order = "order"
    account = "acct"
    authz = "authz"
    challenge = "chall"
    cert = "cert"


class ACMEEndpoint(str, Enum):
    newNonce = "newNonce"
    newOrder = "newOrder"
    order = "order"
    newAccount = "newAcct"
    account = "acct"
    authz = "authz"
    challenge = "chall"
    finalize = "finalize"
    cert = "cert"


class INonceService(abc.ABC):

    @abc.abstractmethod
    def generate(self) -> str:
        """Generate a nonce for use with subsequent ACME requests.

        Returns:
            nonce (str)
        """

    @abc.abstractmethod
    def consume(self, nonce: str) -> bool:
        """Validate and consume the nonce passed in. The nonce must be made invalid for any
        future requests. If consume is called twice the second result must never be True.

        Args:
            nonce (str): The nonce.

        Returns:
            valid (bool): True if the nonce existed in storage and was able to be consumed.
        """


class IAccountService(abc.ABC):

    @abc.abstractmethod
    def create(
        self, resource: models.AccountResource, eab_kid: str = None
    ) -> models.AccountResource:
        """Persist an account resource and the associated jwk to the datastore. If eab_kid is passed in,
        also bind the external account."""

    @abc.abstractmethod
    def get(self, account_id: str) -> models.AccountResource | None:
        pass

    @abc.abstractmethod
    def get_by_jwk(self, jwk: josepy.jwk.JWK) -> models.AccountResource | None:
        pass

    @abc.abstractmethod
    def get_eab_hmac(self, account_id: str) -> str | None:
        pass

    @abc.abstractmethod
    def check_access(
        self, account_id: str, resource_id: str, resource_type: ACMEResourceType
    ) -> bool:
        """Returns True if the account can access the specified resource."""


class IAuthorizationService(abc.ABC):

    @abc.abstractmethod
    def create(
        self, resource: models.AuthorizationResource
    ) -> models.AuthorizationResource:
        """Persist an authorization resource to the datastore. The order passed in is the parent."""

    @abc.abstractmethod
    def update_status(
        self, authz: models.AuthorizationResource, new_state: AuthorizationStatus
    ) -> models.AuthorizationResource:
        pass

    @abc.abstractmethod
    def get(self, authz_id: str) -> models.AuthorizationResource:
        pass

    @abc.abstractmethod
    def get_by_order(self, order_id: str) -> list[models.AuthorizationResource]:
        pass

    @abc.abstractmethod
    def get_by_chall(self, chall_id: str) -> models.AuthorizationResource | None:
        pass


class IOrderService(abc.ABC):

    authorization_service = inject.attr(IAuthorizationService)

    @abc.abstractmethod
    def create(self, resource: models.OrderResource) -> models.OrderResource:
        """Persists an order resource to the datastore. The account passed in is the
        owner and initiator of the request."""

    @abc.abstractmethod
    def update_status(
        self, order: models.OrderResource, new_state: OrderStatus
    ) -> models.OrderResource:
        pass

    @abc.abstractmethod
    def get(self, order_id: str) -> models.OrderResource | None:
        pass

    @abc.abstractmethod
    def process_finalization(
        self, order: models.OrderResource, csr: CertificateSigningRequest
    ) -> models.OrderResource:
        """Processes the CSR asynchronously and updates the datastore order to reflect
        the current state of the order.
        """

    def resolve_state(self, order: models.OrderResource) -> models.OrderResource:
        """Checks and updates the state of an order and its children."""

        def try_transition_order_to(
            order: models.OrderResource, status: OrderStatus
        ) -> tuple[bool, models.OrderResource]:
            # If the order is in a terminal state we leave it alone
            if order.status in [OrderStatus.invalid, OrderStatus.valid]:
                return False, order

            if order.status != status:
                return True, self.update_status(order, status)

            return False, order

        def try_transition_auth_to(
            authz: models.AuthorizationResource, status: AuthorizationStatus
        ) -> tuple[bool, models.AuthorizationStatus]:
            # If the authorization is in a terminal state we leave it alone
            if authz.status in [
                AuthorizationStatus.invalid,
                AuthorizationStatus.revoked,
                AuthorizationStatus.deactivated,
                AuthorizationStatus.expired,
            ]:
                return False, authz

            if authz.status != status:
                return True, self.authorization_service.update_status(authz, status)

            return False, authz

        if order.expires < datetime.now():
            # If the order has expired and has not reached a terminal state, it becomes invalid
            _, order = try_transition_order_to(order, OrderStatus.invalid)

        for authz in order.authorizations:
            # If the authz has expired and has not reached a terminal state, it becomes expired
            if authz.expires < datetime.now():
                _, authz = try_transition_auth_to(authz, AuthorizationStatus.expired)
                _, order = try_transition_order_to(order, OrderStatus.invalid)

            if authz.status in [
                AuthorizationStatus.invalid,
                AuthorizationStatus.revoked,
                AuthorizationStatus.deactivated,
                AuthorizationStatus.expired,
            ]:
                _, order = try_transition_order_to(order, OrderStatus.invalid)

        if order.status == OrderStatus.pending:
            # Now check to see if all authorizations are valid
            if len(order.authorizations) > 0 and all(
                [a.status == AuthorizationStatus.valid for a in order.authorizations]
            ):

                _, order = try_transition_order_to(order, OrderStatus.ready)

        return order


class ICertService(abc.ABC):

    @abc.abstractmethod
    def get(self, ord_id: str) -> CertResource | None:
        """Get the certificate created during order finalization, or none if finalization isn't complete."""


class IChallengeService(abc.ABC):

    authz_service = inject.attr(IAuthorizationService)

    @abc.abstractmethod
    def create(
        self, authz_id: str, chall: models.ChallengeResource
    ) -> models.ChallengeResource:
        """Persist a challenge to the datastore. The authorization passed in is the parent."""

    @abc.abstractmethod
    def update_status(
        self, chall: models.ChallengeResource, new_state: ChallengeStatus
    ) -> models.ChallengeResource:
        pass

    @abc.abstractmethod
    def get(self, chall_id: str) -> models.ChallengeResource | None:
        pass

    @abc.abstractmethod
    def queue_validation(
        self, chall: models.ChallengeResource
    ) -> models.ChallengeResource:
        """Add the challenge to a background processing queue to perform verification at a later date."""

    def validate(
        self,
        acct_jwk: josepy.jwk.JWK,
        order: models.OrderResource,
        authz: models.AuthorizationResource,
        challenge: models.ChallengeResource,
    ) -> models.ChallengeResource:
        """Perform validation of the challenge by ensuring the client has ownership of the domain and persist
        changes to the authentication and challenge resources to the datastore."""

        # TODO: Add threadsafe and challenge status guards

        ChallengeValidator = challenges.validator_for(challenge.type)
        validator = ChallengeValidator(acct_jwk, authz, challenge)
        if validator.validate():
            order_service = inject.instance(IOrderService)
            # The authorization becomes valid
            self.authz_service.update_status(authz, AuthorizationStatus.valid)
            self.update_status(challenge, ChallengeStatus.valid)

            # Get the most up-to-date version of the order
            order = order_service.get(authz.order_id)
            order_service.resolve_state(order)

        return challenge


class IDirectoryService(abc.ABC):

    root_url = "https://change.me/acme"
    external_account_required = False

    url_templates = {
        ACMEEndpoint.newNonce: "newNonce",
        ACMEEndpoint.order: "order/{identifier}",
        ACMEEndpoint.newOrder: "newOrder",
        ACMEEndpoint.finalize: "order/{identifier}/finalize",
        ACMEEndpoint.newAccount: "newAcct",
        ACMEEndpoint.account: "acct/{identifier}",
        ACMEEndpoint.authz: "authz/{identifier}",
        ACMEEndpoint.cert: "cert/{identifier}",
        ACMEEndpoint.challenge: "chall/{identifier}",
    }

    def get_directory(self) -> Mapping[str, Any]:
        """Generates an ACME directory object with supported endpoints and metadata. The format of the
        directory is defined here: https://datatracker.ietf.org/doc/html/rfc8555/#section-7.1.1

        Returns:
            directory (Mapping[str, Any])
        """
        directory = {
            "newAccount": f"{self.root_url}/{self.url_templates[ACMEEndpoint.newAccount]}",
            "newNonce": f"{self.root_url}/{self.url_templates[ACMEEndpoint.newNonce]}",
            "newOrder": f"{self.root_url}/{self.url_templates[ACMEEndpoint.newOrder]}",
            "meta": {
                "externalAccountRequired": self.external_account_required,
                "termsOfService": self.tos_url() or f"{self.root_url}/terms-of-service",
                "website": self.website_url() or f"{self.root_url}",
            },
        }
        random_key = "".join(
            random.choices(string.ascii_letters + string.digits + "-_", k=10)
        )
        directory[random_key] = (
            "https://community.letsencrypt.org/t/adding-random-entries-to-the-directory/33417"
        )

        return directory

    def website_url(self) -> str:
        """Overridable website url returned in the directory meta."""
        pass

    def tos_url(self) -> str:
        """Overridable ToS url returned in the directory meta."""
        pass

    def identifier_from_url(self, endpoint: ACMEEndpoint, url: str) -> str | None:
        """Translates the url in the header of an ACME request to a resource id"""
        url_base = self.root_url
        if not url_base.endswith("/"):
            url_base += "/"

        if parse_result := parse.parse(url_base + self.url_templates[endpoint], url):
            identifier = parse_result.named.get("identifier")
            if not identifier:
                logger.warning(
                    "Unable to extract identifier from url: %s at endpoint %s",
                    url,
                    endpoint.value,
                )
            return parse_result.named.get("identifier")

    def url_for(self, endpoint: ACMEEndpoint, identifier: str = None) -> str:
        """Gets the url for an ACME resource"""
        url_base = self.root_url
        if not url_base.endswith("/"):
            url_base += "/"

        return url_base + self.url_templates[endpoint].format(identifier=identifier)
