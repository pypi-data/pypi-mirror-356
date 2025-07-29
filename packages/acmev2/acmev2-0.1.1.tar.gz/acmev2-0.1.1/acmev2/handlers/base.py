from typing import Any, Generic, Mapping, Optional, Type, TypeVar
from urllib.parse import quote

import inject

from acmev2.messages.base import ACMEMessage
from acmev2.models import ACMEResource
from acmev2.services import IDirectoryService
import logging

logger = logging.getLogger(__name__)


class HttpVerb:
    HEAD = "HEAD"
    GET = "GET"
    POST = "POST"


class ACMERequestHandler:
    allowed_verbs = [HttpVerb.POST]
    message_type: Type[ACMEMessage] = ACMEMessage
    requires_nonce = True

    def __init__(
        self,
        request_url: str,
        verb: HttpVerb,
        headers: Mapping[str, Any] = None,
        msg: Optional[Mapping[str, Any]] = None,
    ):
        self.request_url = request_url
        self.verb = verb
        self.headers = headers or {}
        self.msg = msg

    def extract_message(self, msg: Optional[Mapping[str, Any]]):
        return self.message_type.from_json(msg)

    def process(msg: ACMEMessage) -> "ACMEModelResponse":
        pass


T = TypeVar("T")


class ACMEResponse(Generic[T]):
    content_type: str = "application/json"
    directory_service = inject.attr(IDirectoryService)
    msg: T | None

    def __init__(
        self,
        headers: Mapping[str, Any] = None,
        msg: Optional[T] = None,
        code: int = 200,
        location: str = None,
    ):
        self.headers = headers or {}
        self.msg = msg or None
        self.code = code

        if location:
            self.headers["Location"] = location

        directory_root = self.directory_service.root_url
        self.add_link_header(directory_root, "index")

    def add_link_header(self, link: str, rel: str):
        link_header = self.headers.get("Link", "")

        header_value = f'<{quote(link, safe="/:")}>;rel="{rel}"'
        if link_header:
            link_header += ","

        self.headers["Link"] = link_header + header_value


class ACMEModelResponse(ACMEResponse[ACMEResource]):
    def serialize(self) -> str:
        if self.msg:
            return self.msg.model_dump_json(indent=2)
        else:
            return ""
