#!/usr/bin/env python3
"""Serve this folder over HTTPS so the microphone (getUserMedia) is available.

getUserMedia is only exposed in a secure context: https:// or http://localhost.
Plain http://<lan-ip> will NOT work (navigator.mediaDevices is undefined).

Usage:
    python3 serve.py
Then open the printed https:// URL and accept the self-signed certificate warning.

No third-party packages are required; openssl is used to make a local certificate.
"""

import http.server
import os
import socket
import ssl
import subprocess
import sys

PORT = 8443
HERE = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(HERE, ".devcert.pem")
KEY = os.path.join(HERE, ".devkey.pem")


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return None


def ensure_cert(extra_ips):
    if os.path.exists(CERT) and os.path.exists(KEY):
        return
    sans = ["DNS:localhost", "IP:127.0.0.1", "IP:::1"]
    sans += ["IP:" + ip for ip in extra_ips if ip]
    print("Generating self-signed certificate ...")
    subprocess.check_call(
        [
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
            "-keyout", KEY, "-out", CERT, "-days", "365",
            "-subj", "/CN=localhost",
            "-addext", "subjectAltName=" + ",".join(sans),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main():
    ip = lan_ip()
    ensure_cert([ip])
    os.chdir(HERE)

    httpd = http.server.ThreadingHTTPServer(
        ("0.0.0.0", PORT), http.server.SimpleHTTPRequestHandler
    )
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

    print("Serving %s at:" % HERE)
    print("  https://localhost:%d" % PORT)
    if ip:
        print("  https://%s:%d   (from another device)" % (ip, PORT))
    print("\nAccept the self-signed certificate warning, then allow the mic.")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    sys.exit(main())
