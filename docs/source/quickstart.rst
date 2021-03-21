==========
Quickstart
==========

If you’re just looking to render simple data-less templates, you can get up
and running with the command line:

.. code-block:: console

    $ rost build


This will recursively search ``./templates`` for templates (any file whose name
does not start with ``.`` or ``_``) and build them to ``./dist``.

To monitor your source directory for changes, recompile files if they change,
and start a web server use ``watch``:

.. code-block:: console

    $ rost watch


The ``build`` and ``watch`` each take these common options:

* ``--searchpath``: Sets the directory to look in for templates.
* ``--outputpath``: Sets the directory to place rendered files in.
* ``--staticpath`` (is accepted multiple times): The directory (or directories)
  within searchpath where static files (such  as CSS and JavaScript) are
  stored.

Getting help on version, available commands, arguments or option names:

.. code-block:: console

    $ rost --version
    $ rost --help
    $ rost build --help
    $ rost watch --help
