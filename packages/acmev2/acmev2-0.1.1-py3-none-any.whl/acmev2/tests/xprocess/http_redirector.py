#!/usr/bin/env python

import contextlib
from http.server import (
    BaseHTTPRequestHandler,
    ThreadingHTTPServer,
)
import socket


class Redirector(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(302)
        new_path = "https://%s%s" % (self.headers["host"], self.path)
        self.send_header("Location", new_path)
        self.end_headers()


# ensure dual-stack is not disabled; ref #38907
class DualStackServer(ThreadingHTTPServer):

    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()


httpd = DualStackServer(("0.0.0.0", 80), Redirector)
print("Serving HTTP->HTTPS redirector")
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nKeyboard interrupt received, exiting.")
    exit(0)
