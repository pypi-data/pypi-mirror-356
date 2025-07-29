import inject

from acmev2.errors import ACMEMethodNotAllowedError
from acmev2.messages.base import ACMEMessage
from acmev2.services import INonceService
from .base import ACMERequestHandler, ACMEModelResponse, HttpVerb


class NewNonceRequestHandler(ACMERequestHandler):
    """Returns a new nonce that a client can use on a subsequent request."""

    allowed_verbs = [HttpVerb.GET, HttpVerb.HEAD]
    requires_nonce = False

    @inject.autoparams()
    def process(
        self, msg: ACMEMessage, nonce_service: INonceService = None
    ) -> ACMEModelResponse:
        nonce = nonce_service.generate()

        headers = {"Replay-Nonce": nonce, "Cache-Control": "no-store"}

        if self.verb == HttpVerb.GET:
            code = 204
        elif self.verb == HttpVerb.HEAD:
            code = 200
        else:
            raise ACMEMethodNotAllowedError()

        resp = ACMEModelResponse(headers, code=code)
        return resp
