==========
Quickstart
==========

Eager to get started? This page gives a good introduction to Rost. It assumes
you already have Rost installed. If you do not, head over to the
:doc:`installation` section.


Create a skeleton project
=========================

#. To get start with Rost first, choose a name for your project, create an
   appropriately-named directory, and switch to that directory:

   .. code-block:: console

      $ mkdir project-name
      $ cd project-name

#. Create an ``templates`` directory for you templates, and add a
   ``index.html`` inside:

   .. code-block:: console

      $ mkdir templates
      $ echo "<h1>Rost Example</h1>" >> templates/index.html

#. To build your project use the ``build`` command:

   .. code-block:: console

      $ rost build
      $ open dist/index.html


Rendering templates with the ``rost`` CLI
=========================================

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
  within searchpath where static files (such as CSS and JavaScript) are
  stored.


Starting a development server
=============================

To start a web server, monitor your source directory for changes and recompile
files if they change, use ``watch``:

.. code-block:: console

   $ rost watch


Preview your site by navigating to http://localhost:8080/ in your browser.

By default the ``watch`` command starts an web server bind to ``localhost`` on
port ``8080`` you can use the ``--bind`` and ``--port`` options to set a
different bind or port.

To start a live reload server use the ``--livereload`` option with ``watch``
command:

.. code-block:: console

   $ rost watch --livereload


Getting help on version, commands and option names
==================================================

Getting help on version, available commands, arguments or option names:

.. code-block:: console

   $ rost --version
   $ rost --help
   $ rost build --help
   $ rost watch --help


Next Steps
==========

If the CLI does not satisfy your needs, more advanced configuration can be done
with custom python build scripts using the Rost API. See :doc:`advanced`
section or :doc:`api` section for more details.
