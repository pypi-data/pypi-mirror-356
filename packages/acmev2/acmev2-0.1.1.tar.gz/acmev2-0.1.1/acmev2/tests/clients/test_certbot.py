import inject
from acmev2.handlers import handle, ChallengeRequestHandler
from acmev2.challenges import validator_for
from acmev2.models import (
    OrderResource,
    AccountResource,
    ChallengeStatus,
    AuthorizationStatus,
)
from acmev2.tests.conftest import MessageBuilder
from acmev2.tests.helpers import authz_by_url
from acmev2.services import IChallengeService
from box import Box
import pytest
from xprocess import ProcessStarter
import tempfile
import os


class TestCertbot:

    @pytest.fixture
    def acme_server(self, xprocess):
        app_server = os.path.join(
            os.path.dirname(__file__), "../xprocess/acme_server.py"
        )

        class Starter(ProcessStarter):
            terminate_on_interrupt = True
            timeout = 5
            # startup pattern
            pattern = "Debugger PIN"

            # command to start process
            args = ["uv", "run", app_server]

        # ensure process is running
        xprocess.ensure("acme_server", Starter)

        yield

        # clean up whole process tree afterwards
        xprocess.getinfo("acme_server").terminate()

    @pytest.mark.slow
    def test_certbot(
        self,
        acme_server,
    ):
        import subprocess

        with tempfile.TemporaryDirectory() as cert_root:
            cmd = [
                "certbot",
                "--work-dir",
                cert_root,
                "--logs-dir",
                cert_root + "/logs",
                "--config-dir",
                cert_root + "/config",
                "certonly",
                "-d",
                "acme.localhost",
                "--server",
                "http://localhost:8080/directory",
                "--agree-tos",
                "-m",
                "usr@amce.localhost",
                "--standalone",
                "-n",
            ]

            res = subprocess.run(cmd, capture_output=True)
            assert res.returncode == 0
            assert os.path.exists(
                cert_root + "/config/live/acme.localhost/fullchain.pem"
            )
