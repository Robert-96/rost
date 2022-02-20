============
Installation
============

Use the following command to install ``rost``:

.. code-block:: console

    $ python3 -m pip install rost


To check that ``rost`` was correctly installed run the ``rost`` command with
the ``--version`` flag:

.. code-block:: console

    $ rost --version
    $ python3 -m rost --version  # or invoke the command through the Python interpreter


Living on the edge
==================

If you want to work with the latest code before it’s released, install or
update the code from the ``main`` branch:

.. code-block:: console

    $ python3 -m pip install -U git+https://github.com/Robert-96/rost.git


Upgrade
=======

If you installed a stable release via pip and wish to upgrade to the latest
stable release, you can do so by adding ``--upgrade``:

.. code-block::

    $ python3 -m pip instal --upgrade rost


If you installed Rost via the *“living on the edge“* method, simply perform the
same step to install the most recent version.


How to invoke ``rost``?
=======================

Getting help on version, commands and option names
--------------------------------------------------

.. code-block:: console

    $ rost --version
    $ rost --help
    $ rost build --help
    $ rost watch --help


For more details check out the :doc:`cli` section.


Other ways of calling ``rost``
------------------------------

Calling ``rost`` through through the Python interpreter (``python -m rost``):

.. code-block:: console

    $ python -m rost [...]
    $ python -m rost build


You can also invoke ``rost`` from Python code directly:

.. code-block:: python

    from rost import build, watch


    build()


For more details check out the :doc:`advanced` section, or the :doc:`api`
section.
