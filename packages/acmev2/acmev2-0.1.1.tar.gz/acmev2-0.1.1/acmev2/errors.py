from enum import Enum


ERROR_PREFIX = "urn:ietf:params:acme:error:"

ERROR_CODES = {
    "accountDoesNotExist": "The request specified an account that does not exist",
    "alreadyRevoked": "The request specified a certificate to be revoked that has"
    " already been revoked",
    "badCSR": "The CSR is unacceptable (e.g., due to a short key)",
    "badNonce": "The client sent an unacceptable anti-replay nonce",
    "badPublicKey": "The JWS was signed by a public key the server does not support",
    "badRevocationReason": "The revocation reason provided is not allowed by the server",
    "badSignatureAlgorithm": "The JWS was signed with an algorithm the server does not support",
    "caa": "Certification Authority Authorization (CAA) records forbid the CA from issuing"
    " a certificate",
    "compound": 'Specific error conditions are indicated in the "subproblems" array',
    "connection": ("The server could not connect to the client to verify the domain"),
    "dns": "There was a problem with a DNS query during identifier validation",
    "dnssec": "The server could not validate a DNSSEC signed domain",
    "incorrectResponse": "Response received didn't match the challenge's requirements",
    "invalidContact": "The provided contact URI was invalid",
    "malformed": "The request message was malformed",
    "rejectedIdentifier": "The server will not issue certificates for the identifier",
    "orderNotReady": "The request attempted to finalize an order that is not ready to be finalized",
    "rateLimited": "There were too many requests of a given type",
    "serverInternal": "The server experienced an internal error",
    "tls": "The server experienced a TLS error during domain verification",
    "unauthorized": "The client lacks sufficient authorization",
    "unsupportedContact": "A contact URL for an account used an unsupported protocol scheme",
    "unknownHost": "The server could not resolve a domain name",
    "unsupportedIdentifier": "An identifier is of an unsupported type",
    "externalAccountRequired": "The server requires external account binding",
    "userActionRequired": "User action required",
}


class ACMEError(Exception):
    type: str = "malformed"
    detail: str = None
    code: int = 403
    header_links: list[tuple[str, str]] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        if "type" in kwargs:
            self.type = kwargs["type"]

        if "detail" in kwargs:
            self.detail = kwargs["detail"]

        if "code" in kwargs:
            self.code = kwargs["code"]

        if "header_links" in kwargs:
            self.header_links = kwargs["header_links"]

        if self.type in ERROR_CODES:
            self.type = f"{ERROR_PREFIX}{self.type}"


class ACMEBadNonceError(ACMEError):
    type = "badNonce"
    code = 400


class ACMEUnauthorizedError(ACMEError):
    type = "unauthorized"
    code = 401


class ACMEResourceNotFoundError(ACMEError):
    type = "resourceNotFound"
    code = 404


class ACMEMalformedError(ACMEError):
    type = "malformed"
    detail = "Malformed request"
    code = 400


class ACMESignatureVerificationError(ACMEError):
    type = "malformed"
    detail = "Malformed signature"
    code = 400


class ACMEToSAgreementError(ACMEError):
    type = "userActionRequired"
    code = 403
    detail = "Please read and agree to the terms of service"


class ACMEUserActionRequiredError(ACMEError):
    type = "userActionRequired"
    code = 403

    def __init__(self, detail: str, *args, **kwargs):
        self.detail = detail
        super().__init__(*args, **kwargs)


class ACMEMethodNotAllowedError(ACMEError):
    type = "malformed"
    code = 403


class ACMEBadCSRDetail(str, Enum):
    sansRequired = "SANS are required"
    invalidSan = "Invalid subjectAlternateName extension value"
    cnMissingFromSan = (
        "The common name must also appear in the subjectAlternateName extension"
    )
    csrOrderMismatch = (
        "The CSR must indiciate the exact same set of identifiers as the order"
    )
    orderNotAuthorized = "Order has not completed all authorizations"


class ACMEBadCSRError(ACMEError):
    type = "badCSR"

    def __init__(self, detail: ACMEBadCSRDetail):
        self.detail = str(detail)
        super().__init__()


class ACMEInvalidContentTypeError(ACMEError):
    code = 415


class JoseJsonFormatError(ACMEError):
    pass
