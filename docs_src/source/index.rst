.. _index:

|painto| documentation
========================

.. image:: ../assets/hexagon_rainbow.png
   :width: 100px
   :align: left

A flexible color library for Python with support for multiple color formats,
operations, conversion, and more. Use as a drop-in addition to pillow, pygame,
and more, giving you more options and control with your colors.



Introduction
------------

.. code-block:: console

   (.venv) $ pip install painto

Then open up a python script and try something out like:


.. code-block:: python

   import painto

   print(painto.red)  # prints 'red'
   print(painto.red.hex)  # prints '#FF0000'
   print(painto.red.console("Red text"))

.. raw:: html

   <pre><font color="red">Red text</font></pre>

.. code-block:: console

   print(painto.random_color())

``#9313C0`` |9313C0|


Documentation
-------------

Quick Start
^^^^^^^^^^^

A relatively quick read of the basics of what |painto| can do.

.. toctree::
   :maxdepth: 2

   quickstart


Usage Guide
^^^^^^^^^^^

For a more in-depth look at how to use |painto|, check out the usage guide which
covers all of the features of the library with examples.

.. toctree::
   :maxdepth: 3

   usage


API Reference
^^^^^^^^^^^^^

A reference for the classes and functions in the painto library for a
deeper look at how to use the library.

.. toctree::
   :maxdepth: 3

   api
