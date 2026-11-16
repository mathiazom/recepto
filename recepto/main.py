import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from recipe import process_recipe

FAVICON = (Path(__file__).parent / "favicon.ico").read_bytes()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if path == "/favicon.ico":
            self.respond(FAVICON, "image/x-icon")
            return
        try:
            self.respond(process_recipe(path[1:]).encode(), "text/plain; charset=utf-8")
        except Exception:
            traceback.print_exc()
            self.send_error(500)

    def respond(self, body, content_type):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
