=================
CLI Documentation
=================

If you are looking for information on a specific command, option, or argument,
this part of the documentation covers in more details the command line
interface of Rost.


Invocation
==========

.. code-block:: console

    $ rost [...]


You can also invoke the command through the Python interpreter from the command line:

.. code-block:: console

    $ python3 -m rost [...]


Commands
========

.. click:: rost.cli:cli
   :prog: rost
   :nested: full
