import logging

import inject
import pydantic

from acmev2.errors import (
    ACMEError,
    ACMEBadNonceError,
    ACMEInvalidContentTypeError,
    ACMEMethodNotAllowedError,
    ACMEUnauthorizedError,
)
from acmev2.handlers import ACMEModelResponse, ACMERequestHandler
from acmev2.logging import LazyLoggedResponse
from acmev2.handlers.base import HttpVerb
from acmev2.messages.base import (
    ACMEMessage,
    AuthenticatedACMEMessage,
    SignedACMEMessage,
)
from acmev2.models import AccountStatus, ProblemResource
from acmev2.services import INonceService

logger = logging.getLogger(__name__)


def format_problem(error: ACMEError):
    """Formats an ACMEError as a problem document response.

    Args:
        error (ACMEError): The error to transform.

    Returns:
        ACMEModelResponse: A model response that will serialize to a problem document.
    """
    resp = ACMEModelResponse(
        headers={"Content-Type": "application/problem+json"},
        msg=ProblemResource(type=error.type, detail=error.detail),
        code=error.code,
    )

    for link, rel in error.header_links:
        resp.add_link_header(link, rel)

    return resp


class LazyLoggedMessage:
    def __init__(self, message: ACMEMessage):
        self.message = message

    def __str__(self):
        import json

        if isinstance(self.message, SignedACMEMessage):
            return json.dumps(
                {
                    "payload": self.message.jose_message.payload_decoded,
                    "protected": self.message.jose_message.protected_decoded,
                },
                indent=2,
            )
        else:
            return json.dumps(self.message.body, indent=2)


def handle(req: ACMERequestHandler) -> ACMEModelResponse:
    """Handles the ACME request and any errors it raises, along with
    ensuring every request that needs a nonce has one returned.

    Args:
        req (ACMERequestHandler): The request handler to be executed.

    Returns:
        ACMEModelResponse: A serializable model that an ACME client can understand.
    """
    nonce_service = inject.instance(INonceService)
    resp: ACMEModelResponse = None
    acme_message: ACMEMessage | None = None
    try:
        if (
            req.msg is not None
            and req.verb == HttpVerb.POST
            and req.headers.get("Content-Type") != "application/jose+json"
        ):
            logger.error(
                "Invalid content-type header: %s.", req.headers.get("Content-Type")
            )
            raise ACMEInvalidContentTypeError()

        if req.verb not in req.allowed_verbs:
            logger.error(
                "Invalid verb '%s' for request. Only verbs %s allowed.",
                req.verb,
                req.allowed_verbs,
            )
            raise ACMEMethodNotAllowedError()

        acme_message = req.extract_message(req.msg)
        logger.debug("client message: %s", LazyLoggedMessage(acme_message))

        # Request url integrity: https://datatracker.ietf.org/doc/html/rfc8555/#section-6.4
        if isinstance(acme_message, SignedACMEMessage):
            if acme_message.url != req.request_url:
                logger.error(
                    "Invalid message url. Payload: %s does not match request: %s",
                    acme_message.url,
                    req.request_url,
                )
                raise ACMEUnauthorizedError()

        # Ensure account hasn't been revoked or deactivated
        if isinstance(acme_message, AuthenticatedACMEMessage):
            if acme_message.account.status != AccountStatus.valid:
                logger.error(
                    "Client attempted to use account '%s' but it was not valid."
                )
                raise ACMEError(detail="Account not valid")

        # Consume the nonce right before processing the request
        if req.requires_nonce and not nonce_service.consume(acme_message.nonce):
            raise ACMEBadNonceError()

        resp = req.process(acme_message)

        if resp.content_type:
            resp.headers["Content-Type"] = resp.content_type
    except ACMEError as exc:
        # These are normal expected errors raised by handlers
        logging_extra_info = ""
        if acme_message and isinstance(acme_message, SignedACMEMessage):
            logging_extra_info += f" url<{acme_message.url}>"
        if acme_message and isinstance(acme_message, AuthenticatedACMEMessage):
            logging_extra_info += f" account<{acme_message.account_id}>"

        logging.info(
            f"ACMEError - type<{exc.type}> detail<{exc.detail}>{logging_extra_info}"
        )
        resp = format_problem(exc)
    except pydantic.ValidationError:
        # Pydantic errors usually happen when the request is malformed
        logger.exception("Error validating Pydantic model")
        resp = format_problem(ACMEError(type="malformed"))
    except Exception:
        # All other errors return a generic problem document
        logging.exception("Unhandled exception caught at error boundry")
        resp = format_problem(ACMEError(type="serverInternal", code=500))

    if req.verb == HttpVerb.POST and "Replay-Nonce" not in resp.headers:
        # Every POST needs a nonce returned. Head/Get requests should only
        # generate a nonce with the newNonce handler.
        resp.headers["Replay-Nonce"] = nonce_service.generate()

    logger.debug("response: %s", LazyLoggedResponse(resp))
    return resp
