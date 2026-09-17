#!/usr/bin/env python3
"""Local CORS proxy for the browser demo (prototype_actionable_digest.html).

The demo page is opened as file:// (origin "null"), and local OpenAI-compatible
routers (e.g. localhost:20128) usually don't send Access-Control-Allow-Origin,
so the browser blocks the fetch before it reaches the router. This proxy sits
in between and adds the missing CORS headers.

Usage:
    LLM_BASE_URL='http://localhost:20128/v1' python3 scripts/cors_proxy.py
Then in the demo page, set "Base URL" to http://localhost:8787/v1 instead of
the router's real address (model/key stay the same).
"""
import http.server
import os
import sys
import urllib.error
import urllib.request

TARGET_BASE_URL = os.environ.get("LLM_BASE_URL", "http://localhost:20128/v1")
PROXY_PORT = int(os.environ.get("PROXY_PORT", "8787"))

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
}


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        for k, v in CORS_HEADERS.items():
            self.send_header(k, v)
        self.end_headers()

    def do_POST(self):
        self._forward("POST")

    def do_GET(self):
        self._forward("GET")

    def _forward(self, method):
        target_url = TARGET_BASE_URL.rstrip("/") + self.path
        body = None
        length = self.headers.get("Content-Length")
        if length:
            body = self.rfile.read(int(length))
        headers = {"Content-Type": self.headers.get("Content-Type", "application/json")}
        auth = self.headers.get("Authorization")
        if auth:
            headers["Authorization"] = auth
        req = urllib.request.Request(target_url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                self._send(resp.status, resp.read(), resp.headers.get("Content-Type", "application/json"))
        except urllib.error.HTTPError as e:
            self._send(e.code, e.read(), "application/json")

    def _send(self, status, payload, content_type):
        self.send_response(status)
        for k, v in CORS_HEADERS.items():
            self.send_header(k, v)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        sys.stderr.write("[cors-proxy] " + (fmt % args) + "\n")


def main():
    print(f"CORS proxy: http://localhost:{PROXY_PORT} -> {TARGET_BASE_URL}", flush=True)
    http.server.HTTPServer(("localhost", PROXY_PORT), ProxyHandler).serve_forever()


if __name__ == "__main__":
    main()
