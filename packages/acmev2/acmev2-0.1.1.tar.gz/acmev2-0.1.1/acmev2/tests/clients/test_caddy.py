import time
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
from acmev2.services import IChallengeService, IAccountService
from box import Box
import pytest
from xprocess import ProcessStarter
import tempfile
import os
import asyncio
from acmev2.tests.test_services import MemoryAccountService
import shutil


class TestCaddy:

    CADDYFILE = """
acme.localhost 
  tls {
    ca http://localhost:8080/directory
    ca_root /tmp/acmev2.flask.crt
    eab kid hmac
  }
}
"""

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
    def test_caddy(
        self,
        acme_server,
    ):
        # This works intermittently, but I can't stop Caddy from resolving acme.localhost to ipv6 sometimes through
        # the local DNS resolver, even when it's placed in /etc/hosts

        import subprocess

        with open("/tmp/Caddyfile", "w") as cfg:

            cfg.write(self.CADDYFILE)

        cmd = [
            "caddy",
            "run",
        ]

        proc = subprocess.Popen(cmd, cwd="/tmp")
        cert_loc = os.path.expanduser(
            "~/.local/share/caddy/certificates/localhost-8080-directory/acme.localhost/acme.localhost.crt"
        )
        shutil.rmtree(os.path.expanduser("~/.local/share/caddy/"), ignore_errors=True)

        deadline = time.time() + 5
        cert_found = False
        while time.time() < deadline and not cert_found:
            cert_found = os.path.exists(cert_loc)
            time.sleep(1)

        proc.terminate()
        assert cert_found
