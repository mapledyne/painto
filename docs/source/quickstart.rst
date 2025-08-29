.. _quickstart:

Quick Start
===========


Installation
------------

.. code-block:: console

   (.venv) $ pip install painto

Basic Usage
-----------

.. code-block:: python

    import painto

    # Create colors from names, hex, or RGB values
    red = painto.red
    blue = painto.Color("#0000FF")
    green = painto.Color(0, 255, 0)
    transparent = painto.transparent

    # Basic color properties
    print(red.hex)        # "#FF0000"
    print(red.rgb)        # (255, 0, 0)
    print(red.hsv)        # (0.0, 1.0, 1.0)

    # Color arithmetic
    purple = red + blue
    darker_red = red / 2
    lighter_blue = blue * 2

    # Generate color ranges
    gradient = list(panto.color_range(red, blue, 5))


Choosing Colors
---------------

All color names from w3c/css, the XKCD color list, and others are available:

.. code-block:: python

    # From color names
    red = painto.red
    blue = painto.blue

In some cases, the same color name (e.g. red) is in multiple lists. If you want
a color from a specific list, you can do so by using the list name:

.. code-block:: python

    red = painto.red  # Returns w3c red of #FF0000
    red = painto.xkcd.red  # XKCD red is #E50000


Random Colors
-------------

You can generate a random color from the w3c, xkcd, or other lists:

.. code-block:: python

    new_color = painto.random_color()  # a random color from the entire color space
    new_w3c_color = painto.w3c.random()  # a random color from the w3c list
    new_xkcd_color = painto.xkcd.random()  # a random color from the xkcd list

    new_colors = painto.xkcd.random(10)  # will return a list of colors from the list

Console Usage
-------------

For easy coloring for console output:

.. code-block:: python

    red = painto.red
    print(red.console("Red text"))

    yellow = painto.yellow
    print(yellow.console_bg("Yellow background"))

.. raw:: html

    <pre><span style="color:#f00">Red text</span><br>
    <span style="color:#000;background-color:#FF0;">Yellow background</span></pre>

Note:
    With :meth:`console_bg() <painto.color.Color.console_bg>`, the text color is automatically chosen to be white
    or black, depending on which is more contrasting with the background color.


Color Properties
----------------

You can get the properties of a color:

.. code-block:: python

    color = painto.orange

    print(color.r, color.g, color.b, color.a)  # 255 165 0 255
    print(color.hex)                            # "#FFA500"
    print(color.name)                           # "orange"
    print(color.luminosity)                     # 0.696
    print(color.hsv)                            # (0.108, 1.0, 255)

Color Operations
----------------

You can perform arithmetic operations on colors:

.. code-block:: python

    red = painto.red
    blue = painto.blue

    # Blend colors
    purple = red + blue

    # Scale brightness
    darker = red / 2
    lighter = blue * 2


Color Ranges
------------

You can generate a range of colors between two colors:

.. code-block:: python

    # Generate gradient between colors
    colors = painto.color_range(painto.red, painto.blue, 10)  # 10 steps
    for c in colors:
        print(c.console_bg(c.hex))


.. image:: ../assets/red_to_blue_range.png
    :scale: 50%

.. code-block:: python

    # Inclusive range (includes end color)
    colors = painto.color_range(painto.red, painto.blue, 5, inclusive=True)


.. note::
    For more detailed usage and examples, see the full :ref:`usageguide` section.
