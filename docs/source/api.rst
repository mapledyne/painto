API
===

.. automodule:: painto.color
   :members:

.. automodule:: painto.color_list
   :members:

.. attribute:: painto.transparent

   This is a :class:`Color` object that represents the color ``#00000000`` (fully transparent).
   It can be used as a placename for transparent backgrounds or similar. Any color that ends up
   with an alpha value of 0 will be treated as transparent.

.. attribute:: painto.pride

   This is a :class:`ColorList` of the colors based on the Pride flag [#pride]_. Because the Pride flag
   uses common colors for their flag, if you want to use these specific colors, you'll generally
   want to use the full name to the color (``painto.pride.red``) instead of the short name
   (``painto.red``).

.. [#pride] As taken from https://www.flagcolorcodes.com/pride-rainbow .

.. attribute:: painto.w3c

   This is a :class:`ColorList` of the colors based on the W3C color names.

   The W3C color names are a list of colors that are used in the W3C specification, allowing
   convient use with HTML and CSS. When working with a :class:`Color`, you can return a
   reliable HTML friendly code (either name or hex code) by using :attr:`Color.web`.

   The full list of w3c colors are available here: https://www.w3schools.com/colors/colors_names.asp

   .. note:: For consistency, all |painto| colors are all lower case. The colors names are not
      case sensitive in CSS, so this won't impact their use.


.. attribute:: painto.xkcd

   XKCD color survey collection.

   This is a :class:`ColorList` of the colors based on the XKCD color survey. This dataset contains
   colors with descriptive names that were crowdsourced from the XKCD community,
   providing a rich palette of human-named colors.

   The colors in this collection include:

   * Common color names (red, blue, green, etc.)
   * Descriptive color names (baby blue, blood red, etc.)
   * Humorous or colloquial names (barf green, baby poop, etc.)
   * Technical color names (azure, aquamarine, etc.)

   This collection is particularly useful for:

   * Natural language color processing
   * User-friendly color selection interfaces
   * Data visualization with human-readable color names
   * Applications requiring descriptive color names

   License: Creative Commons Zero 1.0 (Public Domain)
   Source: XKCD Color Survey (https://xkcd.com/color/rgb/)

   .. note::
      Due to the naming conventions used with |painto|, some color names had to
      be changed since things like spaces don't work well as attribute names.
      
      All XKCD names, then, were changed to all lower case, and spaces were removed,
      making "sunflower yellow" become "sunfloweryellow", for example.

      This had the unforunate side effect of causing some naming collisions since
      the list had a distinct "``green blue``" and "``greenblue``" color in the list and
      similar naming collisions. These were all kept, but names of collisions became
      "``greenblue``" and "``greenblue2``" so if you came across the hex code, it would still
      have a name.

   :Example:
      >>> # get 10 random colors with names vs just random r,g,b values
      >>> colors = painto.xkcd.random(10)
      >>> for c in colors:
      ...     print(c.console_bg(c.name))
