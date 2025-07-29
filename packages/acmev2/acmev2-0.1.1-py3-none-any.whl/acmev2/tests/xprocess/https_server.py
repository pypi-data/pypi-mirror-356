#!/usr/bin/env python
from datetime import datetime, timedelta, timezone
from http.server import (
    BaseHTTPRequestHandler,
    SimpleHTTPRequestHandler,
    ThreadingHTTPServer,
)

import os
import socket
import ssl
import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from acmev2.tests.helpers import gen_csr

pkey_path: str = None
cert_path: str = None


def _get_best_family(*address):
    infos = socket.getaddrinfo(
        *address,
        type=socket.SOCK_STREAM,
        flags=socket.AI_PASSIVE,
    )
    family, type, proto, canonname, sockaddr = next(iter(infos))
    return family, sockaddr


def test(
    HandlerClass=BaseHTTPRequestHandler,
    ServerClass=ThreadingHTTPServer,
    protocol="HTTP/1.0",
    port=443,
    bind=None,
):

    ServerClass.address_family, addr = _get_best_family(bind, port)
    HandlerClass.protocol_version = protocol
    with ServerClass(addr, HandlerClass) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f"[{host}]" if ":" in host else host
        print(
            f"Serving HTTPS on {host} port {port} " f"(https://{url_host}:{port}/) ..."
        )
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.verify_mode = ssl.VerifyMode.CERT_NONE
            context.load_cert_chain(cert_path, pkey_path)
            httpd.socket = context.wrap_socket(
                httpd.socket,
                server_side=True,
            )
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == "__main__":
    import argparse
    import contextlib

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        "--directory",
        default=os.getcwd(),
        help="serve this directory " "(default: current directory)",
    )

    args = parser.parse_args()

    pkey_path = os.path.join(args.directory, "key.pem")
    cert_path = os.path.join(args.directory, "crt.pem")
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    csr = gen_csr(key, "localhost", ["localhost"])
    builder = (
        x509.CertificateBuilder()
        .issuer_name(
            x509.Name(
                [
                    x509.NameAttribute(x509.NameOID.COMMON_NAME, "ca.localhost"),
                ]
            )
        )
        .subject_name(csr.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=90))
    )
    cert = builder.sign(key, hashes.SHA256())
    with open(pkey_path, "w") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            ).decode()
        )
    with open(cert_path, "w") as f:
        f.write(cert.public_bytes(encoding=serialization.Encoding.PEM).decode())

    handler_class = SimpleHTTPRequestHandler

    # ensure dual-stack is not disabled; ref #38907
    class DualStackServer(ThreadingHTTPServer):

        def server_bind(self):
            # suppress exception when protocol is IPv4
            # with contextlib.suppress(Exception):
            #    self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

        def finish_request(self, request, client_address):
            self.RequestHandlerClass(
                request, client_address, self, directory=args.directory
            )

    test(HandlerClass=handler_class, ServerClass=DualStackServer, bind="0.0.0.0")
