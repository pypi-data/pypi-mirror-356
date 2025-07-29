from acmev2.models import NewAccountRequestSchema
from .base import SignedACMEMessage


class NewAccountMessage(SignedACMEMessage[NewAccountRequestSchema]):
    """https://datatracker.ietf.org/doc/html/rfc8555/#section-7.3"""
