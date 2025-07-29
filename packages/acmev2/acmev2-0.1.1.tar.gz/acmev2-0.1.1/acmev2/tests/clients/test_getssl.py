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


class TestGetSSL:

    GETSSL_CONFIG = """
# vim: filetype=sh
#
# This file is read first and is common to all domains
#
# Uncomment and modify any variables you need
# see https://github.com/srvrco/getssl/wiki/Config-variables for details
#
# The staging server is best for testing (hence set as default)
SKIP_HTTP_TOKEN_CHECK=true
CA="http://acme.localhost:8080"
CHECK_REMOTE="false"
# This server issues full certificates, however has rate limits
#CA="https://acme-v02.api.letsencrypt.org"
SANS="acme.localhost"
# The agreement that must be signed with the CA, if not defined the default agreement will be used
#AGREEMENT=""

# Set an email address associated with your account - generally set at account level rather than domain.
#ACCOUNT_EMAIL="usr@acme.localhost"
ACCOUNT_KEY_LENGTH=4096
ACCOUNT_KEY="/home/vscode/.getssl/account.key"

# Account key and private key types - can be rsa, prime256v1, secp384r1 or secp521r1
#ACCOUNT_KEY_TYPE="rsa"
PRIVATE_KEY_ALG="rsa"
#REUSE_PRIVATE_KEY="true"

# Preferred Chain - use an different certificate root from the default
# This uses wildcard matching so requesting "X1" returns the correct certificate - may need to escape characters
# Staging options are: "(STAGING) Doctored Durian Root CA X3" and "(STAGING) Pretend Pear X1"
# Production options are: "ISRG Root X1" and "ISRG Root X2"
#PREFERRED_CHAIN="\(STAGING\) Pretend Pear X1"

# Uncomment this if you need the full chain file to include the root certificate (Java keystores, Nutanix Prism)
#FULL_CHAIN_INCLUDE_ROOT="true"

# The command needed to reload apache / nginx or whatever you use.
# Several (ssh) commands may be given using a bash array:
# RELOAD_CMD=('ssh:sshuserid@server5:systemctl reload httpd' 'logger getssl for server5 efficient.')
#RELOAD_CMD=""

ACL=('/tmp/acme/.well-known/acme-challenge')
USE_SINGLE_ACL="true"

# The time period within which you want to allow renewal of a certificate
#  this prevents hitting some of the rate limits.
# Creating a file called FORCE_RENEWAL in the domain directory allows one-off overrides
# of this setting
RENEW_ALLOW="30"

# Define the server type. This can be https, ftp, ftpi, imap, imaps, pop3, pop3s, smtp,
# smtps_deprecated, smtps, smtp_submission, xmpp, xmpps, ldaps or a port number which
# will be checked for certificate expiry and also will be checked after
# an update to confirm correct certificate is running (if CHECK_REMOTE) is set to true
SERVER_TYPE="https"
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

    @pytest.fixture
    def chall_server_root(self, xprocess):
        class Starter(ProcessStarter):
            terminate_on_interrupt = True
            timeout = 5
            # startup pattern
            pattern = "Serving HTTP"

            # command to start process
            args = ["python3", "-m", "http.server", "-d", "/tmp/acme", "80"]

        # ensure process is running and return its logfile
        xprocess.ensure("chall_server", Starter)

        yield

        # clean up whole process tree afterwards
        xprocess.getinfo("chall_server").terminate()

    @pytest.mark.slow
    def _test_getssl(self, acme_server, chall_server_root):
        """This test won't work until getssl releases a fix that sees 'processing' and 'pending' as valid challenge responses"""
        import subprocess

        download_getssl = [
            "curl",
            "--silent",
            "--user-agent",
            "getssl/manual",
            "https://raw.githubusercontent.com/srvrco/getssl/latest/getssl",
            "--output",
            "getssl",
        ]

        getssl_path = "/tmp/getssl"
        if not os.path.exists(getssl_path):
            os.mkdir("/home/vscode/.getssl")
            assert subprocess.run(download_getssl, cwd="/tmp").returncode == 0
            subprocess.run(["chmod", "+x", "/tmp/getssl"])
            subprocess.run(["/tmp/getssl", "-c", "acme.localhost"])
            with open("/home/vscode/.getssl/getssl.cfg", "w") as cfg:
                cfg.write(self.GETSSL_CONFIG)

            os.mkdir("/home/vscode/.getssl/acme.localhost")
            with open("/home/vscode/.getssl/acme.localhost/getssl.cfg") as cfg:
                cfg.write("")

        cmd = ["/tmp/getssl", "acme.localhost", "-U", "-f"]

        res = subprocess.run(cmd, capture_output=True)

        assert res.returncode == 0
        assert os.path.exists("/home/vscode/.getssl/acme.localhost/acme.localhost.crt")
