from acmev2.models import ChallengeResource
from acmev2.services import ACMEResourceType, ACMEEndpoint
from .base import SignedACMEMessage, AuthenticatedACMEMessage, WithResourceUrl


class ChallengeMessage(SignedACMEMessage, WithResourceUrl[ChallengeResource]):
    """https://datatracker.ietf.org/doc/html/rfc8555/#section-7.5.1"""

    protected_resource_type = ACMEResourceType.challenge
    protected_url_type = ACMEEndpoint.challenge
