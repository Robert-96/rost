import threading
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler


class WebServer:
    """Create a very basic webserver serving files relative to the given directory."""

    def __init__(self, bind="localhost", port=8080, directory="."):
        self.bind = bind
        self.port = port
        self.directory = directory

        self.server_address = (self.bind, self.port)

    def _target(self, server_address, directory):
        httpd = HTTPServer(server_address, partial(SimpleHTTPRequestHandler, directory=directory))
        httpd.serve_forever()

    def start(self):
        self.thread = threading.Thread(target=self._target, args=(self.server_address, self.directory), daemon=True)
        self.thread.start()

    def stop(self):
        self.thread.join(0)
