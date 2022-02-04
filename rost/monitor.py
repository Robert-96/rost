from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer


class FileMonitor:
    """Creates an observer thread that is watching directories and dispatches callback calls."""

    def __init__(self, monitorpaths, callback):
        self.monitorpaths = monitorpaths
        self.callback = callback

    def __repr__(self):
        return "{}({!r}, {!r})".format(type(self).__name__, self.monitorpaths, self.callback)

    def _handler(self):
        try:
            self.callback()
        except Exception:
            pass

    def start(self):
        """Start the file monitor service."""

        self.event_handler = LoggingEventHandler()

        self.event_handler.on_created = self._handler
        self.event_handler.on_deleted = self._handler
        self.event_handler.on_modified = self._handler

        self.observer = Observer()

        for path in self.monitorpaths:
            self.observer.schedule(self.event_handler, path, recursive=True)

        self.observer.start()

    def stop(self):
        """Stops the file monitor service."""

        self.observer.stop()
        self.observer.join()


if __name__ == "__main__":
    import logging
    import time

    monitor = FileMonitor(["dist"], lambda: logging.info("Callback called."))
    monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
