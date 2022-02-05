from pathlib import Path
import threading

import requests

from rost.server import WebServer


def test_happy_flow(tmpdir):
    tmpdir = Path(tmpdir)
    html = '<h1>Hello, world!</h1>'

    with open(Path(tmpdir, 'index.html'), 'w') as fp:
        fp.write(html)

    bind = "localhost"
    port = 5005

    server = WebServer(root=tmpdir, bind=bind, port=port)

    thread = threading.Thread(target=server.serve, daemon=True)
    thread.start()

    response = requests.get('http://{}:{}/'.format(bind, port))
    assert response.status_code == 200
    assert response.text == html

    thread.join(0)
