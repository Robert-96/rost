import re
from pathlib import Path
import os.path

from rost.generator import Rost, build


def test_happy_flow(tmpdir):
    searchpath = Path(".", "example", "templates")
    outputpath = Path(tmpdir, "dist")
    staticpaths = ["static"]

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths)
    rost.build()

    assert searchpath.is_dir()
    assert outputpath.is_dir()
    assert Path(outputpath, "index.html").is_file()

    for static in staticpaths:
        assert Path(outputpath, static).exists()


def test_build(tmpdir):
    searchpath = Path(".", "example", "templates")
    outputpath = Path(tmpdir, "dist")
    staticpaths = ["static"]

    build(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths)

    assert searchpath.is_dir()
    assert outputpath.is_dir()
    assert Path(outputpath, "index.html").is_file()

    for static in staticpaths:
        assert Path(outputpath, static).exists()


def test_context(tmpdir):
    searchpath = Path(".", "tests", "data", "templates")
    outputpath = Path(tmpdir, "dist")
    staticpaths = ["static"]

    context = {
        "title": "Rost - Integration Tests"
    }
    filters = {
        "hello": lambda x: x
    }

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths,
                context=context, filters=filters)
    rost.build()

    index = Path(outputpath, "index.html")
    assert index.is_file()

    with open(index) as fp:
        data = fp.read()

    match = re.search(r'<h1 id="title">Rost - Integration Tests</h1>', data)
    assert match is not None


def test_contexts(tmpdir):
    searchpath = Path(".", "tests", "data", "templates")
    outputpath = Path(tmpdir, "dist")
    staticpaths = ["static"]

    filters = {
        "hello": lambda x: x
    }
    context = {
        "title": "Rost - Integration Tests"
    }
    contexts = [
        ("index.html", context)
    ]

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths,
                contexts=contexts, filters=filters)
    rost.build()

    index = Path(outputpath, "index.html")
    assert index.is_file()

    with open(index) as fp:
        data = fp.read()

    match = re.search(r'<h1 id="title">Rost - Integration Tests</h1>', data)
    assert match is not None


def test_filters(tmpdir):
    searchpath = Path(".", "tests", "data", "templates")
    outputpath = Path(tmpdir, "dist")
    staticpaths = ["static"]

    context = {
        "title": "Rost - Integration Tests"
    }
    filters = {
        "hello": lambda x: "Hello, {}!".format(x)
    }

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths,
                context=context, filters=filters)
    rost.build()

    index = Path(outputpath, "index.html")
    assert index.is_file()

    with open(index) as fp:
        data = fp.read()

    match = re.search(r'<h1 id="title">Hello, Rost - Integration Tests!</h1>', data)
    assert match is not None
