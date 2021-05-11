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


Global Context
--------------

The simplest way to supply data to the template is to pass a mapping from
variable names to their values (a *“context”*) as the ``context`` keyword
argument to the ``build`` or ```watch`` functions.

.. code-block:: python

    # build.py

    from rost import build


    # A context that should be available all the time to all templates.
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


Template Specific Context
-------------------------

If you want to pass data to a specific template you can use the ``contexts``
keyword argument off the ``build`` and ``watch`` functions.

.. code-block:: python

    # build.py

    from rost import build


    # A context that should be available all the time to all templates.
    context = {
        "title": "Rost Example"
    }

    # A list of "regex, context" pairs. Each context is either a dictionary or a
    # function that takes either no argument or or the current template as its sole
    # argument and returns a dictionary. The regex, if matched against a filename,
    # will cause the context to be used.
    contexts = [
        ("*.html", {}),
    ]


    if __name__ == "__main__":
        build(
            searchpath="templates",
            outputpath="dist",
            staticpaths=["static"],
            context=context,
            contexts=contexts
        )


By default ``rost`` will use only the first matching context, if you want to use all matching
contexts call the ``build`` or ``watch`` functions with the ``merge_contexts`` set to ``True``.

.. code-block:: python

    # build.py

    from rost import build


    # A context that should be available all the time to all templates.
    context = {
        "title": "Rost Example"
    }

    # A list of "regex, context" pairs. Each context is either a dictionary or a
    # function that takes either no argument or or the current template as its sole
    # argument and returns a dictionary. The regex, if matched against a filename,
    # will cause the context to be used.
    contexts = [
        ("*.html", {}),
        ("index.html", {})
    ]


    if __name__ == "__main__":
        build(
            searchpath="templates",
            outputpath="dist",
            staticpaths=["static"],
            context=context,
            contexts=contexts,
            merge_contexts=True
        )


Custom Filters
==============

Inside the templates variables can be modified by `filters <https://jinja.palletsprojects.com/en/2.11.x/templates/#filters>`_. All the standard Jinja2 filters are supported (you can found the full list `here <https://jinja.palletsprojects.com/en/2.11.x/templates/#builtin-filters>`_). To add your own filters, simply pass your as the ``filters`` keyword argument to the ``build`` and ``watch`` functions.

.. code-block:: python

    # build.py

    from rost import build


    filters = {
        "hello": lambda x: "Hello, {}!".format(x)
    }


    if __name__ == "__main__":
        build(
            searchpath="templates",
            outputpath="dist",
            staticpaths=["static"],
            filters=filters
        )


Then you can use them in your templates as you would expect:

.. code::

    {{ 'World'|hello }}
