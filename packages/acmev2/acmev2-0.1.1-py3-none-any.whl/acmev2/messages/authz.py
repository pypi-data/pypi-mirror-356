from acmev2.models import AuthorizationResource, AuthorizationSchema
from acmev2.services import ACMEResourceType, ACMEEndpoint
from .base import SignedACMEMessage, WithResourceUrl


class AuthorizationMessage(
    SignedACMEMessage[AuthorizationSchema],
    WithResourceUrl[AuthorizationResource],
):
    """https://datatracker.ietf.org/doc/html/rfc8555/#section-7.5"""

    protected_resource_type = ACMEResourceType.authz
    protected_url_type = ACMEEndpoint.authz
