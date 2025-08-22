import random

from .color import Color


class ColorList(dict):
    """A collection of Color objects to create a named collection (e.g. w3c, xkcd, etc.)

    This class extends the built-in dict class to provide a convenient way to store and access
    Color objects. The colors can be accessed both as dictionary items and as attributes.

    Example:
        >>> colors = painto.w3c  # One of the built-in color lists.
        >>> color = colors.random()  # Returns a single random color.

        >>> my_colors = ColorList({
        ...     "red": Color("#e40303"),
        ...     "orange": Color("#ff8c00"),
        ...     "yellow": Color("#ffed00"),
        ... ...
        ... })

        >>> my_colors.random(3)  # Returns a list of 3 random colors.
        >>> my_colors.random()  # Returns a single random color.


    """

    def __init__(self, *args: str, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)
        self.__dict__ = self
    
    def random(self, count: int = 1) -> Color | list[Color]:
        """Returns random color(s) from this color list.

        Args:
            count (int, optional): Number of random colors to return. Defaults to 1.

        Returns:
            Color: If count==1, returns a single Color object.
            list[Color]: If count>1, returns a list of Color objects.

        Raises:
            ValueError: If count is greater than the number of available colors.
        """
        if count == 1:
            return random.choice(list(self.values()))
        return random.sample(list(self.values()), count)
