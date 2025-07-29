from typing import Type
from .http import Http01ChallengeValidator
from .base import ChallengeValidator
from .custom import CustomChallengeValidatorRunner, CustomChallengeValidator
from acmev2.models import ChallengeType


def validator_for(typ: ChallengeType) -> Type[ChallengeValidator]:
    match typ:
        case ChallengeType.http_01:
            return Http01ChallengeValidator
        case ChallengeType.custom:
            return CustomChallengeValidatorRunner

    raise Exception("No match found for challenge type {typ}")
