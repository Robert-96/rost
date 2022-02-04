from livereload import Server


class LiveReloader:
    """Initialize a livereload server and watch file changes.

    Args:

    """

    def __init__(self, monitorpaths, callback, root=".", bind="localhost", port=5050):
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
        try:
            self.callback()
        except Exception:
            pass

    def serve(self):
        server = Server()

        for path in self.monitorpaths:
            server.watch(path, self._handler)

        server.serve(host=self.bind, port=self.port, root=self.root)

    def start(self):
        pass

    def stop(self):
        pass


if __name__ == "__main__":
    import logging

    reloader = LiveReloader(["dist"], lambda: logging.info("Callback called."))
    reloader.start()
