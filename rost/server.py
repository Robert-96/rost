from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler


class WebServer:
    """Create a very basic webserver serving files relative to the given directory."""

    def __init__(self, root=".", bind="localhost", port=8080):
        self.root = root
        self.bind = bind
        self.port = port

        self.server_address = (self.bind, self.port)

    def __repr__(self):
        return "{}({!r}, {!r}, {!r})".format(
            type(self).__name__,
            self.root,
            self.bind,
            self.port
        )

    def serve(self):
        httpd = HTTPServer(self.server_address, partial(SimpleHTTPRequestHandler, directory=self.root))
        httpd.serve_forever()


if __name__ == "__main__":
    server = WebServer(root="dist", bind="localhost", port=8080)
    server.server()
