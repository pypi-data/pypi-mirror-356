from __future__ import annotations

import copy
import json
from typing import Any, Callable, Generator, Mapping, TypeVar

import josepy
from pydantic import (
    BaseModel,
    NaiveDatetime,
    PlainSerializer,
    computed_field,
    model_serializer,
)
from typing_extensions import Annotated


class ACMEResource(BaseModel):
    _exclude_fields: list[Callable[[], Generator[str, None, None]]] = []

    def __init_subclass__(cls, **kwargs):
        exclude_fields: list[Callable[[], Generator[str, None, None]]] = []
        for subclass in cls.mro():
            if "exclude_fields" in subclass.__dict__:
                exclude_fields.append(getattr(subclass, "exclude_fields"))

        def new_init(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._exclude_fields = exclude_fields

        cls.__init__ = new_init

        super().__init_subclass__(**kwargs)

    @model_serializer(mode="wrap")
    def serialize(self, handler):
        result = handler(self)
        for func in self._exclude_fields:
            for field in func(self):
                if field in result:
                    del result[field]

        return result


class JoseJsonSchema(ACMEResource):
    payload: str
    protected: str
    signature: str

    @computed_field
    @property
    def payload_decoded(self) -> Mapping[str, Any]:
        try:
            return json.loads(josepy.decode_b64jose(self.payload).decode())
        except json.JSONDecodeError:
            return {}

    @computed_field
    @property
    def protected_decoded(self) -> Mapping[str, Any]:
        try:
            return json.loads(josepy.decode_b64jose(self.protected).decode())
        except json.JSONDecodeError:
            return {}


class EmptyMessageSchema(ACMEResource):
    pass


RFC3339Date = Annotated[
    NaiveDatetime,
    PlainSerializer(
        lambda _datetime: _datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), return_type=str
    ),
]

T = TypeVar("T", bound=ACMEResource)


def without(obj: T, attrs: list[str]) -> T:
    new_obj = copy.copy(obj)
    new_obj._exclude_fields = copy.copy(obj._exclude_fields)
    new_obj._exclude_fields.append(lambda *_: (a for a in attrs))

    return new_obj
