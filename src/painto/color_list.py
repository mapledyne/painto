import random

from .color import Color


class ColorList(dict[str, Color]):
    """A collection of Color objects to create a named collection (e.g. w3c, xkcd, etc.)

    This class extends the built-in dict class to provide a convenient way to store and access
    Color objects. The colors can be accessed both as dictionary items and as attributes.

    :example:
        >>> colors = painto.w3c  # One of the built-in color lists.
        >>> color = colors.random()  # Returns a single random color from the w3c list.

        >>> my_colors = ColorList({
        ...     "red": Color("#e40303"),
        ...     "orange": Color("#ff8c00"),
        ...     "yellow": Color("#ffed00"),
        ... ...
        ... })

        >>> my_colors.random(3)  # Returns a list of 3 random colors.
        >>> my_colors.random()  # Returns a single random color from the list.

    .. note::
        Most use cases won't ever need to create your own list - this class mainly
        exists to give easier access to the built-in color lists. See :ref:`colorlists`
        for the lists and how to use them.

    """

    def __init__(self, *args: str, **kwargs: str) -> None:
        name = ''
        if 'name' in kwargs:
            name = kwargs.pop('name')
        super().__init__(*args, **kwargs)
        self.__dict__ = self
        self.set_metadata(source=name)

    def __setitem__(self, name: str, value: Color) -> None:
        super().__setitem__(name, value)
        self.set_metadata(name)

    def set_metadata(self, name: str = '', source: str = '') -> None:
        if name:
            color_list = [name]
        else:
            color_list = list(self.keys())

        if not source and len(self) > 1:
            first_color = next(iter(self))
            source = self[first_color].source

        for color_name in color_list:
            metadata = {'name': color_name}
            if source:
                metadata['source'] = source
            self[color_name].set_metadata(metadata)



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
            return random.choice(list(self.values()))  # noqa: S311
        return random.sample(list(self.values()), count)
