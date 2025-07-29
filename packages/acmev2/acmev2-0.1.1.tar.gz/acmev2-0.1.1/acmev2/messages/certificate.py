from acmev2.models import NewOrderRequestSchema, OrderFinalizationRequestSchema
from acmev2.models import CertResource
from acmev2.services import ACMEResourceType, ACMEEndpoint
from .base import SignedACMEMessage, AuthenticatedACMEMessage, WithResourceUrl


class CertMessage(
    SignedACMEMessage[NewOrderRequestSchema],
    WithResourceUrl[CertResource],
):
    """https://datatracker.ietf.org/doc/html/rfc8555/#section-7.4.2"""

    protected_resource_type = ACMEResourceType.cert
    protected_url_type = ACMEEndpoint.cert
