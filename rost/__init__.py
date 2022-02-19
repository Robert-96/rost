"""Rost is simple static site generator based on Jinja2 with a command line interface build using Click."""

import logging

from .generator import Rost, build, watch  # noqa: F401


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
