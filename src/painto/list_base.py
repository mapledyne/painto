from .color import Color
from .color_list import ColorList

base_colors = ColorList({
    "black": Color("#000000"),
    "white": Color("#FFFFFF"),
    "red": Color("#FF0000"),
    "green": Color("#00FF00"),
    "blue": Color("#0000FF"),
    "yellow": Color("#FFFF00"),
    "cyan": Color("#00FFFF"),
    "magenta": Color("#FF00FF"),
}, name="base")
