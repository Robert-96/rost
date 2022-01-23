import threading

from livereload import Server


class LiveReloader:
    """Creates an observer thread that is watching directories, refresh the browser using livereload and dispatches callback calls."""

    def __init__(self, outputpath, monitorpaths, callback, bind="localhost", port=5050):
        self.outputpath = outputpath
        self.monitorpaths = monitorpaths
        self.callback = callback

        self.bind = bind
        self.port = port

    def _handler(self):
        try:
            self.callback()
        except Exception:
            pass

    def start(self):
        server = Server()

        for path in self.monitorpaths:
            server.watch(path, self._handler)

        server.serve(host=self.bind, port=self.port, root=self.outputpath)

    def stop(self):
        pass


if __name__ == "__main__":
    import logging

    reloader = LiveReloader(["dist"], lambda : logging.info("Callback called."))
    reloader.start()
