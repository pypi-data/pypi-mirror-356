from datetime import datetime

import inject

from acmev2.errors import (
    ACMEError,
)
from acmev2.messages import ChallengeMessage
from acmev2.models import AuthorizationResource, ChallengeStatus
from acmev2.services import (
    ACMEEndpoint,
    IAuthorizationService,
    IChallengeService,
    IDirectoryService,
)

from .base import ACMEModelResponse, ACMERequestHandler
import logging

logger = logging.getLogger(__name__)


class ChallengeRequestHandler(ACMERequestHandler):
    """Begins validating a specific challenge. Validation can be done in-line or
    the service implementer can decide to periodically validate in the background."""

    message_type = ChallengeMessage
    directory_service = inject.attr(IDirectoryService)
    challenge_service = inject.attr(IChallengeService)
    authorization_service = inject.attr(IAuthorizationService)

    def process(self, msg: ChallengeMessage):
        logger.debug(
            "Handling request to queue challenge %s for processing", msg.resource.id
        )
        chall = msg.resource
        authz = self.authorization_service.get(chall.authz_id)
        self.validate_expiration(msg, authz)

        if chall.status == ChallengeStatus.pending:
            logger.debug("Queueing challenge %s for processing", msg.resource.id)
            chall = self.challenge_service.queue_validation(chall)
            chall.status = ChallengeStatus.processing

        resp = ACMEModelResponse(msg=chall, code=200)
        resp.add_link_header(
            self.directory_service.url_for(ACMEEndpoint.authz, authz.id), "up"
        )

        return resp

    def validate_expiration(self, msg: ChallengeMessage, authz: AuthorizationResource):
        if datetime.now() > authz.expires:
            logger.debug("Challenge %s had expired", msg.resource.id)
            raise ACMEError(detail="Authorization has expired")
