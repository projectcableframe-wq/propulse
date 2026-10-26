#!/usr/bin/env python3
"""Static server for the propeller-selector preview.

Serves app/ on 0.0.0.0 and adds a forced-download route, because a plain
`python3 -m http.server` serves HTML inline and some browsers then save the
rendered page instead of the file itself.

Routes
    GET /               -> app/index.html (redirect to the application)
    GET /<file>         -> the file, inline (normal preview behaviour)
    GET /download       -> the application as an attachment
                           (Content-Disposition: filename=...)

Standard library only.  Usage:
    python3 tools/preview_server.py [port] [--directory app]
"""
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(os.path.dirname(ROOT), "app")
DOWNLOAD_FILE = "yanmar_engine_propeller_selector.html"


def make_handler(directory):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=directory, **kw)

        def do_GET(self):
            if self.path.split("?")[0] in ("/download", "/download/"):
                return self._send_download()
            return super().do_GET()

        def do_HEAD(self):
            if self.path.split("?")[0] in ("/download", "/download/"):
                return self._send_download(head=True)
            return super().do_HEAD()

        def _send_download(self, head=False):
            path = os.path.join(directory, DOWNLOAD_FILE)
            if not os.path.exists(path):
                self.send_error(404, "application file not found")
                return
            size = os.path.getsize(path)
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Disposition",
                             'attachment; filename="%s"' % DOWNLOAD_FILE)
            self.send_header("Content-Length", str(size))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if head:
                return
            with open(path, "rb") as f:
                while True:
                    chunk = f.read(64 * 1024)
                    if not chunk:
                        break
                    self.wfile.write(chunk)

        def log_message(self, fmt, *args):
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    return Handler


def main():
    port = 8080
    directory = APP_DIR
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--directory" and i + 1 < len(args):
            directory = os.path.abspath(args[i + 1]); i += 2
        else:
            port = int(args[i]); i += 1
    directory = os.path.abspath(directory)
    srv = ThreadingHTTPServer(("0.0.0.0", port), make_handler(directory))
    print("serving %s on 0.0.0.0:%d  (download: /download)" % (directory, port), flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
