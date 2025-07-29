import inject
from acmev2.handlers import handle, ChallengeRequestHandler
from acmev2.challenges import validator_for
from acmev2.models import (
    OrderResource,
    AccountResource,
    ChallengeStatus,
    AuthorizationStatus,
)
from acmev2.tests.conftest import MessageBuilder, default_request_headers
from acmev2.tests.helpers import authz_by_url
from acmev2.services import IChallengeService
from box import Box
import pytest
from xprocess import ProcessStarter
import tempfile
import os
import josepy


class TestChallengeRequest:

    @pytest.fixture
    def chall_server_root(self, xprocess):
        with tempfile.TemporaryDirectory() as srv_root:

            class Starter(ProcessStarter):
                timeout = 5
                terminate_on_interrupt = True
                # startup pattern
                pattern = "Serving HTTP"

                # command to start process
                args = ["python3", "-m", "http.server", "-d", srv_root, "80"]

            # ensure process is running and return its logfile
            xprocess.ensure("chall_server", Starter)

            yield srv_root

            # clean up whole process tree afterwards
            xprocess.getinfo("chall_server").terminate(timeout=2)

    @pytest.fixture
    def https_chall_server_root(self, xprocess):
        https_server = os.path.join(
            os.path.dirname(__file__), "../xprocess/https_server.py"
        )
        with tempfile.TemporaryDirectory() as srv_root:

            class Starter(ProcessStarter):
                terminate_on_interrupt = True
                timeout = 5
                # startup pattern
                pattern = "Serving HTTPS"

                # command to start process
                args = ["uv", "run", https_server, "-d", srv_root]

            # ensure process is running and return its logfile
            xprocess.ensure("https_chall_server", Starter)

            yield srv_root

            # clean up whole process tree afterwards
            xprocess.getinfo("https_chall_server").terminate(timeout=2)

    @pytest.fixture
    def http_to_https_redirector(self, xprocess):
        http_server = os.path.join(
            os.path.dirname(__file__), "../xprocess/http_redirector.py"
        )

        class Starter(ProcessStarter):
            terminate_on_interrupt = True
            timeout = 5
            # startup pattern
            pattern = "Serving HTTP->HTTPS redirector"

            # command to start process
            args = ["uv", "run", http_server]

        # ensure process is running and return its logfile
        xprocess.ensure("redirector", Starter)

        yield

        # clean up whole process tree afterwards
        xprocess.getinfo("redirector").terminate(timeout=2)

    @pytest.mark.slow
    def test_http_01_server_down(
        self,
        default_order: OrderResource,
        default_account: AccountResource,
        message_builder: MessageBuilder,
    ):
        authz_resource = default_order.authorizations[0]
        chall = authz_resource.challenges[0]

        chall_request = message_builder(acct_id=default_account.id, url=chall.url)

        response = handle(
            ChallengeRequestHandler(
                chall.url, "POST", msg=chall_request, headers=default_request_headers()
            )
        )
        resource = Box(response.msg.model_dump())
        assert resource.status == "processing"
        assert resource.type == "http-01"

        chall_service = inject.instance(IChallengeService)
        chall_service.validate(
            default_account.jwk, default_order, authz_resource, chall
        )

        assert chall.status != ChallengeStatus.valid

    @pytest.mark.slow
    def test_http_01_chall(
        self,
        default_order: OrderResource,
        default_account: AccountResource,
        message_builder: MessageBuilder,
        chall_server_root,
    ):
        authz_resource = default_order.authorizations[0]
        chall = authz_resource.challenges[0]

        chall_request = message_builder(acct_id=default_account.id, url=chall.url)

        response = handle(
            ChallengeRequestHandler(
                chall.url, "POST", msg=chall_request, headers=default_request_headers()
            )
        )
        resource = Box(response.msg.model_dump())
        assert resource.status == "processing"
        assert resource.type == "http-01"

        chall_service = inject.instance(IChallengeService)
        chall_service.validate(
            default_account.jwk, default_order, authz_resource, chall
        )

        assert chall.status != ChallengeStatus.valid

        acme_chall_dir = os.path.join(chall_server_root, ".well-known/acme-challenge/")
        os.makedirs(acme_chall_dir)
        with open(os.path.join(acme_chall_dir, chall.token), "w") as chall_file:
            chall_file.write(
                f"{chall.token}.{josepy.encode_b64jose(default_account.jwk.thumbprint())}"
            )

        chall_service.validate(
            default_account.jwk, default_order, authz_resource, chall
        )

        assert chall.status == ChallengeStatus.valid
        assert chall.validated is not None
        assert authz_resource.status == AuthorizationStatus.valid

    @pytest.mark.slow
    def test_http_01_chall_invalid_cert(
        self,
        default_order: OrderResource,
        default_account: AccountResource,
        message_builder: MessageBuilder,
        https_chall_server_root,
        http_to_https_redirector,
    ):
        authz_resource = default_order.authorizations[0]
        chall = authz_resource.challenges[0]

        chall_request = message_builder(acct_id=default_account.id, url=chall.url)

        response = handle(
            ChallengeRequestHandler(
                chall.url, "POST", msg=chall_request, headers=default_request_headers()
            )
        )
        resource = Box(response.msg.model_dump())
        assert resource.status == "processing"
        assert resource.type == "http-01"

        ValidatorType = validator_for(chall.type)
        validator = ValidatorType(default_account.jwk, authz_resource, chall)

        acme_chall_dir = os.path.join(
            https_chall_server_root, ".well-known/acme-challenge/"
        )
        os.makedirs(acme_chall_dir)
        with open(os.path.join(acme_chall_dir, chall.token), "w") as chall_file:
            chall_file.write(
                f"{chall.token}.{josepy.encode_b64jose(default_account.jwk.thumbprint())}"
            )

        assert validator.validate()
