from acmev2.models import NewOrderRequestSchema, OrderFinalizationRequestSchema
from acmev2.models import OrderResource
from acmev2.services import ACMEResourceType, ACMEEndpoint
from .base import SignedACMEMessage, AuthenticatedACMEMessage, WithResourceUrl


class NewOrderMessage(
    SignedACMEMessage[NewOrderRequestSchema], AuthenticatedACMEMessage
):
    """https://datatracker.ietf.org/doc/html/rfc8555/#section-7.4"""


class OrderFinalizationMessage(
    SignedACMEMessage[OrderFinalizationRequestSchema],
    WithResourceUrl[OrderResource],
):
    """https://datatracker.ietf.org/doc/html/rfc8555/#section-7.5"""

    protected_resource_type = ACMEResourceType.order
    protected_url_type = ACMEEndpoint.finalize


class OrderMessage(
    SignedACMEMessage[NewOrderRequestSchema],
    WithResourceUrl[OrderResource],
):
    """https://datatracker.ietf.org/doc/html/rfc8555/#section-7.4"""

    protected_resource_type = ACMEResourceType.order
    protected_url_type = ACMEEndpoint.order
