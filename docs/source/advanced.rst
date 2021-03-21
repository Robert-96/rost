==============
Advanced Usage
==============

This part of the documentation covers some of ``rost``’s more advanced
features.


.. contents:: Table of Contents
    :local:
    :backlinks: none


Using Custom Build Scripts
==========================

The command line shortcut is convenient, but sometimes your project needs
something different than the defaults. To change them, you can use a build
script.

A minimal build script looks something like this:

.. code-block:: python

    # build.py

    from rost import build


    if __name__ == "__main__":
        build(
            searchpath="templates",
            outputpath="dist",
            staticpaths=["static"]
        )


Finally, just save the script as build.py (or something similar) and run it
with your Python3 interpreter.

.. code-block:: console

    $ python3 build.py


Loading Data
============

The simplest way to supply data to the template is to pass a mapping from
variable names to their values (a *“context”*) as the ``context`` keyword
argument to the ``build`` or ```watch`` functions.

.. code-block:: python

    # build.py

    from rost import build


    context = {
        "title": "Rost Example"
    }


    if __name__ == "__main__":
        build(
            searchpath="templates",
            outputpath="dist",
            staticpaths=["static"],
            context=context
        )


If you want to pass data to a specific template you can use the ``contexts``
keyword argument off the ``build`` and ``watch`` functions.

.. code-block:: python

    # build.py

    from rost import build


    # base context used for all templates
    context = {
        "title": "Rost Example"
    }

    # template specific context
    # keys - regex matching the template name
    # values - the context for the template or group of templates
    contexts = {
        "*.html": {}
    }


    if __name__ == "__main__":
        build(
            searchpath="templates",
            outputpath="dist",
            staticpaths=["static"],
            context=context,
            contexts=contexts
        )


Custom Filters
==============

Inside the templates variables can be modified by `filters <https://jinja.palletsprojects.com/en/2.11.x/templates/#filters>`_. All the standard Jinja2 filters are supported (you can found the full list `here <https://jinja.palletsprojects.com/en/2.11.x/templates/#builtin-filters>`_). To add your own filters, simply pass your as the ``filters`` keyword argument to the ``build`` and ``watch`` functions.

.. code-block:: python

    # build.py

    from rost import build


    filters = {
        "hello": lambda x: "Hello, {}!"
    }


    if __name__ == "__main__":
        build(
            searchpath="templates",
            outputpath="dist",
            staticpaths=["static"],
            filters=filters
        )


Then you can use them in your template as you would expect:

.. code::

    {{ 'World'|hello }}
