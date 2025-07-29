from acmev2.handlers import ACMEModelResponse


import json


class LazyLoggedResponse:
    def __init__(self, resp: ACMEModelResponse):
        self.resp = resp

    def __str__(self):
        return json.dumps(
            {
                "code": self.resp.code,
                "headers": self.resp.headers,
                "msg": (self.resp.msg.model_dump() if self.resp.msg else None),
            },
            indent=2,
        )
