import logging
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler


logger = logging.getLogger(__name__)


class WebServer:
    """This class creates a server that serves files from the directory directory and below, or the current directory
    if directory is not provided, directly mapping the directory structure to HTTP requests.

    Args:
        root (:obj:`str` or :obj:`Path`, optional): A directory relative to which it should serve the files. Defaults to ``.``.
        bind (:obj:`str`, optional): A specific address to which the server should bind. Defaults to ``localhost``.
        port (:obj:`int`, optional): A specific port to which the server should lissen. Defaults to ``8080``.

    """

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
        """Start the server."""

        logger.info("Serving on http//{}:{}/".format(self.bind, self.port))

        httpd = HTTPServer(self.server_address, partial(SimpleHTTPRequestHandler, directory=self.root))
        httpd.serve_forever()


if __name__ == "__main__":
    server = WebServer(root="dist", bind="localhost", port=8080)
    server.server()
