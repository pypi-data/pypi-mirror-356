import abc
import inject
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from acmev2.settings import ACMESettings
from .base import ChallengeValidator
import logging

logger = logging.getLogger(__name__)


class CustomChallengeValidatorRunner(ChallengeValidator):

    def validate(self) -> bool:
        validator = inject.instance(CustomChallengeValidator)
        return validator.validate(self)


class CustomChallengeValidator(abc.ABC):

    @abc.abstractmethod
    def validate(self, challenge_validator: ChallengeValidator) -> bool:
        pass
