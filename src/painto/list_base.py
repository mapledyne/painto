from .color import Color
from .color_list import ColorList

base_colors = ColorList({
    "black": Color("#000000", name="black", source="base"),
    "white": Color("#FFFFFF", name="white", source="base"),
    "red": Color("#FF0000", name="red", source="base"),
    "green": Color("#00FF00", name="green", source="base"),
    "blue": Color("#0000FF", name="blue", source="base"),
    "yellow": Color("#FFFF00", name="yellow", source="base"),
    "cyan": Color("#00FFFF", name="cyan", source="base"),
    "magenta": Color("#FF00FF", name="magenta", source="base"),
})