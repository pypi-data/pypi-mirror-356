import inject
import josepy.jwk

from acmev2.models import AuthorizationResource, HTTPChallengeResource
from acmev2.settings import ACMESettings


class ValidationError(Exception):
    pass


class ChallengeValidator:

    settings = inject.attr(ACMESettings)

    def __init__(
        self,
        acct_jwk: josepy.jwk.JWK,
        authz: AuthorizationResource,
        chall: HTTPChallengeResource,
    ):
        self.chall = chall
        self.authz = authz
        self.acct_jwk = acct_jwk

    def validate(self) -> bool:
        return False
