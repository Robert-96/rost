import time
import unittest.mock as mock
from pathlib import Path

from rost.monitor import FileMonitor


def test_happy_flow(tmpdir):
    tmpdir = Path(tmpdir)
    callback = mock.Mock(spec=callable)
    monitor = FileMonitor([tmpdir], callback)
    monitor.start()

    file = Path(tmpdir, 'test.log')
    file.touch()
    file.unlink()

    # Wait for events to trigger
    time.sleep(5)

    monitor.stop()

    assert callback.called
