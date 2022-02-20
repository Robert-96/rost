================================
Welcome to Rost's documentation!
================================

Rost is a simple static site generator based on Jinja2_ with a command line
interface build using Click_.

Get started with :doc:`installation` and then get a quick overview with the
:doc:`quickstart` section. There is also a :doc:`advanced` section that covers
some of ``rost``’s more advanced features.


Overview
========

Rost’s feature highlights include:

* Includes a simple CLI tool to (re)generate your site build using Click_.
* Includes support for monitor your source directory for changes, and
  regenerates your site if they change.
* Includes a developments server.
* It also includes support for LiveReload_.


Documentation
=============

This part of the documentation guides you through all of the library’s usage
patterns.

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   advanced
   api
   cli
   changelog
   license


.. toctree::
    :caption: Useful Links:

    Source Code <https://github.com/Robert-96/rost>
    PyPi Release <https://pypi.org/project/rost/>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Jinja2: https://jinja.palletsprojects.com/en/2.11.x/
.. _Click: https://click.palletsprojects.com/en/7.x/
.. _LiveReload: https://livereload.readthedocs.io/en/latest/
