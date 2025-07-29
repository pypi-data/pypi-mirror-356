import inject
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from acmev2.settings import ACMESettings
from .base import ChallengeValidator, ValidationError
import logging
import josepy

logger = logging.getLogger(__name__)


class Http01ChallengeValidator(ChallengeValidator):

    def validate(self) -> bool:
        settings = inject.instance(ACMESettings)
        # Only DNS identifiers supported
        domain = f"http://{self.authz.identifier.value}"

        endpoint = f"{domain}/.well-known/acme-challenge/{self.chall.token}"
        logger.info(f"Validating endpoint <{endpoint}> for challenge <{self.chall.id}>")
        expected_content = (
            f"{self.chall.token}.{josepy.encode_b64jose(self.acct_jwk.thumbprint())}"
        )

        try:
            # warnings can sometimes be treated as errors, we need to allow the challenge
            # to run against certificates that are expired
            urllib3.disable_warnings(InsecureRequestWarning)
            challenge_headers = requests.utils.default_headers()
            challenge_headers["User-Agent"] = settings.http_01_challenge_user_agent
            # again, pass verify=False because this challenge should succeed on invalid certs
            # if the challenge is redirected to https
            challenge_response = requests.get(
                endpoint, allow_redirects=True, verify=False
            )

            if challenge_response.status_code != 200:
                error_message = (
                    f"{challenge_response.status_code} status code returned from server"
                )
                logger.debug("Chall %s: " + error_message, self.chall.id)
                raise ValidationError(error_message)

            logger.info(
                f"Challenge returned: <{challenge_response}>, expected: <{expected_content}>"
            )
        except requests.RequestException as exc:
            logger.exception("Error validating http-01 challenge")
            raise ValidationError(
                f"{exc.__class__.__name__}: error requesting {exc.request.url}"
            )

        # remove extra text returned
        actual = challenge_response.text.splitlines()[0].strip()
        if actual != expected_content:
            raise ValidationError("Content did not match expected token")

        return actual == expected_content
