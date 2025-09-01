from .color_list import ColorList
from .list_xkcd import xkcd

rainbow = ColorList({
    "red": xkcd["red"],
    "orange": xkcd["orange"],
    "yellow": xkcd["yellow"],
    "green": xkcd["green"],
    "blue": xkcd["blue"],
    "indigo": xkcd["indigo"],
    "violet": xkcd["violet"],
}, name="rainbow")
