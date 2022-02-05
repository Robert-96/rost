import logging

from livereload import Server


logger = logging.getLogger(__name__)


class LiveReloader:
    """Initialize a livereload server and watch file changes.

    Args:
        monitorpaths (:obj:`list`): A list of paths to monitor.
        callback (:obj:`callable`): A callable to call when a file from ``monitorpaths`` changes.
        root (optional, :obj:`str` or :obj:`Path`): Defaults to ``.``.
        bind (optional, :obj:`str`): Defaults to ``localhost``.
        port (optional, :obj:`int`): Defaults to ``8080``.

    """

    def __init__(self, monitorpaths, callback, root=".", bind="localhost", port=8080):
        self.monitorpaths = monitorpaths
        self.callback = callback

        self.root = root
        self.bind = bind
        self.port = port

    def __repr__(self):
        return "{}({!r}, {!r}, {!r}, {!r}, {!r})".format(
            type(self).__name__,
            self.monitorpaths,
            self.callback,
            self.root,
            self.bind,
            self.port
        )

    def _handler(self):
        logger.info("Handler called.")

        try:
            self.callback()
        except Exception:
            logger.error("Unexpected error occurred while calling the callback function.")

    def serve(self):
        server = Server()

        for path in self.monitorpaths:
            server.watch(path, self._handler)

        logger.info("Serving on http//{}:{}/".format(self.bind, self.port))
        server.serve(host=self.bind, port=self.port, root=self.root)

    def start(self):
        """This methods does't do anything. It's only propose is to comform with the Monitor interface."""

    def stop(self):
        """This methods does't do anything. It's only propose is to comform with the Monitor interface."""


if __name__ == "__main__":
    import logging

    reloader = LiveReloader(["dist"], lambda: logging.info("Callback called."))
    reloader.start()
