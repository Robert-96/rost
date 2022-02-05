import logging

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer


logger = logging.getLogger(__name__)


class FileMonitor:
    """This class creates an observer thread that is watching the provided directories and dispatches callback calls.

    Args:
        monitorpaths (:obj:`list` of :obs:`Path`): A list of paths to monitor.
        callback (:obj:`callable`): A callable to call when a file from ``monitorpaths`` changes.

    """

    def __init__(self, monitorpaths, callback):
        self.monitorpaths = monitorpaths
        self.callback = callback

        self.observer = None

    def __repr__(self):
        return "{}({!r}, {!r})".format(type(self).__name__, self.monitorpaths, self.callback)

    def _handler(self, event):
        logger.info("Handler called with event: {!r}".format(event))

        try:
            self.callback()
        except Exception:
            logger.error("Unexpected error occurred while calling the callback function.")

    def start(self):
        """Start the file monitor service."""

        event_handler = LoggingEventHandler()

        event_handler.on_created = self._handler
        event_handler.on_deleted = self._handler
        event_handler.on_modified = self._handler

        self.observer = Observer()

        for path in self.monitorpaths:
            self.observer.schedule(event_handler, path, recursive=True)

        self.observer.start()

    def stop(self):
        """Stops the file monitor service."""

        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None


if __name__ == "__main__":
    import time

    monitor = FileMonitor(["dist"], lambda: logging.info("Callback called."))
    monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
