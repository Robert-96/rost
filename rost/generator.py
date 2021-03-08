"""Simple static site generator based on Jinja2."""

import os
import re
import time
import shutil
import inspect

import click
from jinja2 import Environment, FileSystemLoader

from .monitor import FileMonitor
from .server import WebServer


def _has_argument(func):
    """Test whether a function expects an argument.

    Args:
        func: The function to be tested for existence of an argument.
    """

    sig = inspect.signature(func)
    return bool(sig.parameters)


class Rost:
    """Simple Jinja2 static page generator."""

    def __init__(self, searchpath="templates", outputpath="dist", staticpaths=None, context=None, filters=None,
                 contexts=None, merge_contexts=False, before_callback=None, after_callback=None):
        self.searchpath = searchpath
        self.outputpath = outputpath
        self.staticpaths = staticpaths or []

        self.contexts = contexts or []
        self.merge_contexts = merge_contexts

        self.filters = filters or {}

        self.before_callback = before_callback
        self.after_callback = after_callback

        self.env = Environment(
            loader=FileSystemLoader(self.searchpath),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.env.filters.update(self.filters)

    def __repr__(self):
        return "{}('{}', '{}')".format(type(self).__name__, self.searchpath, self.outputpath)

    @property
    def template_names(self):
        return self.env.list_templates(filter_func=self.is_template)

    @property
    def templates(self):
        for template_name in self.template_names:
            yield self.get_template(template_name)

    def get_template(self, template_name):
        try:
            return self.env.get_template(template_name)
        except UnicodeDecodeError as e:
            raise UnicodeError('Unable to decode {}: {}'.format(template_name, e))

    def get_context(self, template):
        context = {}
        for regex, context_generator in self.contexts:
            if re.match(regex, template.name):
                if inspect.isfunction(context_generator):
                    if _has_argument(context_generator):
                        context.update(context_generator(template))
                    else:
                        context.update(context_generator())
                else:
                    context.update(context_generator)

                if not self.merge_contexts:
                    break

        return context

    def is_static(self, template_name):
        """Check if a template is a static template. Static templates are copied,
        rather than compiled using Jinja2.

        A template is considered static if it lives in any of the directories
        specified in ``staticpaths``.
        """

        return any(template_name.startswith(path) for path in self.staticpaths)

    def is_partial(self, template_name):
        """Check if a template is a partial template."""

        return any((path.startswith("_") for path in template_name.split("/")))

    def is_ignored(self, template_name):
        """Check if a template should be ignored."""

        return any((path.startswith(".") for path in template_name.split("/")))

    def is_template(self, filename):
        """Check if a file is a template."""

        if self.is_partial(filename):
            return False
        if self.is_ignored(filename):
            return False
        if self.is_static(filename):
            return False

        return True

    def clear_build(self):
        """Clear previous build."""

        shutil.rmtree(self.outputpath, ignore_errors=True)
        os.mkdir(self.outputpath)

    def copy_assets(self):
        """Copy static assets such as CSS or JavaScript."""

        for path in self.staticpaths:
            source = os.path.join(self.searchpath, path)
            target = os.path.join(self.outputpath, path)

            if os.path.isdir(source):
                shutil.copytree(source, target)
            if os.path.isfile(source):
                shutil.copy2(source, target)

    def render_template(self, template):
        """Render a Jinja2 template."""

        filepath = os.path.join(self.outputpath, template.name)
        template.stream(self.get_context(template)).dump(filepath)

    def render_templates(self):
        """Render the Jinja2 templates."""

        for template in self.templates:
            self.render_template(template)

    def build(self):
        self.clear_build()

        if self.before_callback:
            self.before_callback(searchpath=self.searchpath, outputpath=self.outputpath)

        self.copy_assets()
        self.render_templates()

        if self.after_callback:
            self.after_callback(searchpath=self.searchpath, outputpath=self.outputpath)

    def watch(self, monitorpaths=None):
        self.build()

        monitorpaths = monitorpaths or []
        reloader = FileMonitor([self.searchpath, *monitorpaths], self.build)
        reloader.start()

        server = WebServer(directory=self.outputpath)
        server.start()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            reloader.stop()
            server.stop()