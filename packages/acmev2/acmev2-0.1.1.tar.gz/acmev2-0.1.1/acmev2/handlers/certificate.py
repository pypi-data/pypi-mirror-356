import inject

from acmev2.messages import (
    CertMessage,
)
from acmev2.services import (
    IOrderService,
    IAuthorizationService,
    IDirectoryService,
)
from acmev2.models import CertResource
from .base import ACMERequestHandler, ACMEResponse
import logging

logger = logging.getLogger(__name__)


class ACMECertResponse(ACMEResponse[CertResource]):
    content_type = "application/pem-certificate-chain"

    def serialize(self) -> str:
        # TODO: return different certs depending on the
        # client Accept header.
        #  application/pkix-cert - DER
        #  application/pkcs7-mime - DER
        return self.msg.pem


class CertRequestHandler(ACMERequestHandler):
    """Returns a certificate chain for the requested identifier. Only supports
    PEM-encoded certificates."""

    message_type = CertMessage
    order_service = inject.attr(IOrderService)
    directory_service = inject.attr(IDirectoryService)
    authorization_service = inject.attr(IAuthorizationService)

    def process(
        self,
        msg: CertMessage,
    ):
        cert = msg.resource

        return ACMECertResponse(msg=cert, code=200)
