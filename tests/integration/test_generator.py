import os.path

from rost.generator import Rost


def test_happy_flow(tmpdir):
    searchpath = "{}/example/templates".format(os.path.abspath('.'))
    outputpath = "{}/dist".format(tmpdir)
    staticpaths=["static"]

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths)
    rost.build()

    assert os.path.isdir(searchpath)
    assert os.path.isdir(outputpath)
    assert os.path.isfile("{}/index.html".format(outputpath))

    for static in staticpaths:
        assert os.path.exists("{}/{}".format(outputpath, static))