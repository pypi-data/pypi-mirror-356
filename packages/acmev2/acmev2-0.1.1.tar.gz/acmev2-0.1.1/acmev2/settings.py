from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta
from importlib.metadata import version, PackageNotFoundError

try:
    acmev2_version = version("acmev2")
except PackageNotFoundError:
    acmev2_version = "dev"


class Challenges(str, Enum):
    custom = "custom"
    http_01 = "http-01"


class ACMESettings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False, env_prefix="ACMEV2_")

    # If this is true all new accounts will require external account bindings
    eab_required: bool = False

    # Max number of identifiers that can be passed into a new order request
    max_identifiers: int = 50

    # How long the client should wait between polling attempts. This is
    # sent as a Retry-After header
    authorization_client_delay: int = 15

    # The server will refuse to issue domains for any identities in this list. It
    # supports regular expressions.
    blacklisted_domains: list[str] = []

    # How long should the order and authorization objects be valid
    # for after generating?
    resource_expiration_delta: timedelta = timedelta(hours=8)

    # Default set of challenges created when an authorization is created.
    challenges_available: list[Challenges] = [Challenges.http_01]

    # The user agent the http-01 challenge validator will use when requesting the
    # challenge document from the client server.
    http_01_challenge_user_agent: str = f"python-acmev2/{acmev2_version}"

    # Any order requests from this user agent will mask the processing state as pending
    mask_order_processing_status_ua_match: str = "^cert-manager-clusterissuers.*"
