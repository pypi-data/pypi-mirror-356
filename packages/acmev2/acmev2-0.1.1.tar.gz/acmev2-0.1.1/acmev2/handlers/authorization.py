import inject
from acmev2.errors import ACMEError
from acmev2.messages import AuthorizationMessage
from acmev2.models import AuthorizationStatus
from acmev2.services import IAuthorizationService
from acmev2.settings import ACMESettings
from .base import ACMERequestHandler, ACMEModelResponse
import logging

logger = logging.getLogger(__name__)


class AuthorizationRequestHandler(ACMERequestHandler):
    """Returns an authorization and all the associated challenges."""

    message_type = AuthorizationMessage
    authorization_service = inject.attr(IAuthorizationService)
    settings = inject.attr(ACMESettings)

    def process(self, msg: AuthorizationMessage):
        authz_resource = msg.resource
        logger.debug("Processing authz request for resource %s", msg.resource.id)

        if self.should_deactivate(msg):
            authz_resource = self.authorization_service.update_status(
                authz_resource, AuthorizationStatus.deactivated
            )

        headers = {"Retry-After": self.settings.authorization_client_delay}

        return ACMEModelResponse(headers=headers, msg=authz_resource, code=200)

    def should_deactivate(self, msg: AuthorizationMessage) -> bool:
        if msg.payload.status == AuthorizationStatus.deactivated:
            if msg.resource.status == AuthorizationStatus.valid:
                return True

            # Invalid, cannot transition to deactivated from any state but valid
            raise ACMEError(
                detail=f"May not transition to '{AuthorizationStatus.deactivated.value}' from '{msg.resource.status.value}'"
            )

        return False
