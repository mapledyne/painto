import colorsys
import random
from collections.abc import Iterator
from enum import Enum, auto

from .exceptions import ColorNotFoundError, ColorRangeError, RequestsRequiredError

ANSI_RESET = "\033[0m"

class ColorSort(Enum):
    HUE = auto()
    LUMINOSITY = auto()

SORT_BY = ColorSort.LUMINOSITY
DYNAMIC_NAME_LOOKUP = False

class Color(tuple):
    """A color class that represents RGBA colors and supports various operations.

    The Color class can be initialized from:
    - Color names (e.g., "red", "blue")
    - Hex strings (e.g., "#FF0000" or "#FF0000FF")
    - RGB/RGBA tuples (e.g., (255, 0, 0) or (255, 0, 0, 255))

    Features:
    - Arithmetic operations (+, *, /) for color blending and brightness adjustment
    - Comparison operations for sorting by brightness
    - Properties for accessing components (r, g, b, a, rgb, rgba, hex, name)
    - Conversion methods for different color formats

    Example:
        >>> red = Color("red")
        >>> blue = Color("#0000FF")
        >>> purple = red + blue
        >>> darker_purple = purple / 2
    """

# region Dunder functions

    def __new__(cls, *args:int, **kwargs:str) -> 'Color':
        """
        Initialize a Color instance.

        Args can be:
            - Single str arg: Color name or hex string
            - Single tuple arg: RGB(A) tuple
            - Three ints: r,g,b values
            - Four ints: r,g,b,a values

        Kwargs can include:
            name: Optional name for the color
            source: Optional source identifier
        """
        color_rgb = (0, 0, 0, 255)
        if len(args) == 1:
            value = args[0]
            if isinstance(value, str):
                if value.startswith("#"):  # Handle hex string
                    color_rgb = _rgba_from_hex(value)
                else:  # Handle color name
                    color_rgb = _rgba_from_name(value)
            elif not isinstance(value, tuple) or len(value) not in {3, 4}:
                raise ValueError("Single argument must be a color name, hex string, or RGB(A) tuple")
            else:
                color_rgb = value
        elif len(args) in {3, 4}:
            for _, arg in enumerate(args):
                if not isinstance(arg, int | float):
                    raise ValueError("All arguments must be numbers.")
            color_rgb = args
        else:
            raise ValueError("Invalid arguments. Must be a color name, hex string, RGB(A) tuple, or 3-4 RGB(A) values")

        a = 255
        if len(color_rgb) == 4:
            a = color_rgb[3]

        # this makes (1000, 200, 100) turn in to a sensible color
        color_rgb = _redistribute_rgb(color_rgb[0], color_rgb[1], color_rgb[2], a)

        if 'name' in kwargs:
            cls._name = kwargs['name']
        if 'source' in kwargs:
            cls._source = kwargs['source']
        if "escape" in kwargs:
            cls._escape = kwargs['escape']
        if a == 255:
            return super().__new__(cls, color_rgb[0:3])
        return super().__new__(cls, (*color_rgb, a))


    def __repr__(self) -> str:
        a = ""
        if self.a != 255:
            a = f", a={self.a}"
        return f"Color(r={self.r}, g={self.g}, b={self.b}{a})"

    def __str__(self) -> str:
        return self.name

    def __add__(self, other: object) -> tuple[int, ...]:
        """Blend two colors by averaging their RGBA values."""
        if isinstance(other, Color):
            r = (self.r + other.r) // 2
            g = (self.g + other.g) // 2
            b = (self.b + other.b) // 2
            a = (self.a + other.a) // 2
            return Color(r, g, b, a)
        if isinstance(other, tuple):
            if len(other) in {3, 4}:
                r = (self.r + other[0]) // 2
                g = (self.g + other[1]) // 2
                b = (self.b + other[2]) // 2
                if len(other) == 4:
                    a = (self.a + other[3]) // 2
                return r, g, b, a
            return NotImplemented
        if isinstance(other, str):
            try:
                color_from_name = _rgba_from_name(other)
            except ColorNotFoundError:
                return NotImplemented
            return self + color_from_name

        return NotImplemented

    def __radd__(self, other: object) -> tuple[int, ...]:
        return self + other

    def __eq__(self, other: object) -> bool:
        """Compare two colors for equality."""
        if isinstance(other, Color):
            return self.rgba == other.rgba

        if isinstance(other, str):
            try:
                if other.startswith("#"):  # Handle hex string
                    color_from_str = _rgba_from_hex(other)
                else:  # Handle color name
                    color_from_str = _rgba_from_name(other)
            except (ColorNotFoundError, ValueError):
                return False
            return self == color_from_str

        if isinstance(other, tuple):
            if len(other) == 3:
                return self.rgb == other
            if len(other) == 4:
                return self.rgba == other
            return False
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __mul__(self, other: object) -> 'Color':
        """Multiply the color by a factor (will lighten/darken the color)."""
        if isinstance(other, int | float):

            r = int(self.r * other)
            g = int(self.g * other)
            b = int(self.b * other)

            return Color(*_redistribute_rgb(r, g, b))

        return NotImplemented

    def __rmul__(self, other) -> 'Color':  # type: ignore # noqa: ANN001
        if isinstance(other, int | float):
            return self * other
        return NotImplemented

    def __truediv__(self, other) -> 'Color':  # type: ignore # noqa: ANN001
        if isinstance(other, int | float):
            return self * (1 / other)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(self))

    # Compare colors by brightness
    def __lt__(self, other) -> bool:  # type: ignore # noqa: ANN001
        if isinstance(other, Color):
            if SORT_BY == ColorSort.HUE:
                return self.h < other.h
            if SORT_BY == ColorSort.LUMINOSITY:
                return self.luminosity < other.luminosity
        return NotImplemented

    def __le__(self, other) -> bool:  # type: ignore # noqa: ANN001
        if isinstance(other, Color):
            if SORT_BY == ColorSort.HUE:
                return self.h <= other.h
            if SORT_BY == ColorSort.LUMINOSITY:
                return self.luminosity <= other.luminosity
        return NotImplemented

    def __gt__(self, other) -> bool:  # type: ignore # noqa: ANN001
        if isinstance(other, Color):
            if SORT_BY == ColorSort.HUE:
                return self.h > other.h
            if SORT_BY == ColorSort.LUMINOSITY:
                return self.luminosity > other.luminosity
        return NotImplemented

    def __ge__(self, other) -> bool:  # type: ignore # noqa: ANN001
        if isinstance(other, Color):
            if SORT_BY == ColorSort.HUE:
                return self.h >= other.h
            if SORT_BY == ColorSort.LUMINOSITY:
                return self.luminosity >= other.luminosity
        return NotImplemented

    def __neg__(self) -> 'Color':
        return self.difference(Color(255, 255, 255))

    def __bool__(self) -> bool:
        return self.a > 0

    def __int__(self) -> int:
        return (self.r << 16) + (self.g << 8) + self.b

# endregion Dunder functions

# region Public properties

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        return self.r, self.g, self.b, self.a

    @property
    def r(self) -> int:
        return self[0]

    @property
    def g(self) -> int:
        return self[1]

    @property
    def b(self) -> int:
        return self[2]

    @property
    def a(self) -> int:
        if len(self) == 4:
            return self[3]
        return 255

    @property
    def rgb(self) -> tuple[int, int, int]:
        return self.r, self.g, self.b

    @property
    def hls(self) -> tuple[float, float, float]:
        if not hasattr(self, "_hls"):
            self._hls = colorsys.rgb_to_hls(*self.rgb)
        return self._hls

    @property
    def hsv(self) -> tuple[float, float, float]:
        if not hasattr(self, "_hsv"):
            self._hsv = colorsys.rgb_to_hsv(*self.rgb)
        return self._hsv

    @property
    def h(self) -> float:
        return self.hsv[0]

    @property
    def s(self) -> float:
        return self.hsv[1]

    @property
    def v(self) -> float:
        return self.hsv[2]

    @property
    def luminosity(self) -> float:
        if not hasattr(self, "_luminosity"):
            self._luminosity = self.grayscale.r / 255
        return self._luminosity

    @property
    def grayscale(self) -> 'Color':
        if not hasattr(self, "_grayscale"):
            gray = round(0.2126 * self.r + 0.7152 * self.g + 0.0722 * self.b)
            self._grayscale = Color(gray, gray, gray, self.a)
        return self._grayscale

    @property
    def hex(self) -> str:
        """Return the color as a hex string."""
        if not hasattr(self, "_hex"):
            hex_str = f"#{self.r:02X}{self.g:02X}{self.b:02X}"
            if self.a != 255:
                hex_str += f"{self.a:02X}"
            self._hex = hex_str
        return self._hex

    @property
    def name(self) -> str:
        """Return the friendly name if it exists, otherwise the hex value."""
        if hasattr(self, "_name"):
            if self._name.startswith("#") and DYNAMIC_NAME_LOOKUP:
                delattr(self, "_name")

        if not hasattr(self, "_name"):
            if self.a == 0:
                self._name = "transparent"
            else:
                # Check for a friendly name in the reverse lookup
                # Search through color lists for a matching RGB value
                for color_list in color_lists:
                    for name, color in color_list.items():
                        if color.rgb == self.rgb:
                            self._name = name
                            self._source = color.source
                            break
                if not hasattr(self, "_name"):
                    if DYNAMIC_NAME_LOOKUP:
                        self._name = name_lookup(self)
                        if self._name == "unknown":
                            self._name = self.hex
                        else:
                            self._source = "Color.pizza"
                    else:
                        self._name = self.hex
        return self._name

    @property
    def source(self) -> str:
        if not hasattr(self, "_source"):
            self._source = ""
        return self._source

    @property
    def foreground(self) -> 'Color':
        """ Presuming self is the background color, return a contrasting
        foreground color for text. Will return black or white, whichever is
        is more visible on the background.
        """
        if not hasattr(self, "_foreground"):
            if self.luminosity > 0.5:
                self._foreground = Color(0, 0, 0)
            else:
                self._foreground = Color(255, 255, 255)
        return self._foreground

    @property
    def ansi_escape(self) -> str:
        """Gets the ANSI escape sequence for setting text color.

        Returns:
            str: ANSI escape sequence that sets text foreground color to this color.

        Example:
            >>> red = Color("red")
            >>> print(f"{red.ansi_escape}This text is red{red.ansi_reset}")

        This can be combined with ansi_escape_bg to set a background color and text color.

        Example:
            >>> red = Color("red")
            >>> black = Color("black")
            >>> print(f"{red.ansi_escape_bg}{black.ansi_escape}A red background with black text{red.ansi_reset}")
        """
        if not hasattr(self, "_console"):
            self._console = f"\033[38;2;{self.r};{self.g};{self.b}m"
        return self._console

    @property
    def ansi_escape_bg(self) -> str:
        """Gets the ANSI escape sequence for setting background color to this color.

        Returns:
            str: ANSI escape sequence that sets background color to this color.

        Example:
            >>> red = Color("red")
            >>> print(f"{red.ansi_escape_bg}This text has a red background{red.ansi_reset}")

        This can be combined with ansi_escape to set a background color and text color.

        Example:
            >>> red = Color("red")
            >>> black = Color("black")
            >>> print(f"{red.ansi_escape_bg}{black.ansi_escape}A red background with black text{red.ansi_reset}")

        """
        if not hasattr(self, "_console_bg"):
            self._console_bg = f"\033[48;2;{self.r};{self.g};{self.b}m"
        return self._console_bg

    @property
    def ansi_reset(self) -> str:
        """Gets the ANSI escape sequence to reset colors.
        This is the same for all colors, so it's just a convenient alias. Without putting
        this in your console output the colors will persist until the next color change
        onto future lines.

        Returns:
            str: ANSI escape sequence that resets all colors to default.

        Example:
            >>> red = Color("red")
            >>> print(f"{red.ansi_escape_bg}This text has a red background{red.ansi_reset}")

        """
        return ANSI_RESET

# endregion Public properties

# region Public functions


    def console(self, text: str, background: 'Color' = None) -> str:
        """Wraps text with ANSI escape sequences to display it in this color as the
        foreground/text color. This function also wraps the text with the reset to
        put the colors back to normal after the text.

        Args:
            text: The text to colorize.
            background: The background color to use. If not provided, the background will be left
            as the default console background color.

        Returns:
            str: The text wrapped with ANSI escape sequences to display in this color.

        Example:
            >>> red = Color("red")
            >>> print(red.console("This text is red"))
        """
        fg_color = self.ansi_escape
        if background is None:
            return f"{fg_color}{text}{ANSI_RESET}"

        bg_color = background.ansi_escape_bg
        return f"{bg_color}{fg_color}{text}{ANSI_RESET}"

    def console_bg(self, text: str) -> str:
        """Wraps text with ANSI escape sequences to display it with this background color.

        The text color will be automatically set to either black or white depending on
        the background color's luminosity for best contrast.

        Args:
            text: The text to display on the colored background.

        Returns:
            str: The text wrapped with ANSI escape sequences for background and foreground colors.

        Example:
            >>> red = Color("red")
            >>> print(red.console_bg("This text has a red background"))
        """
        bg_color = self.ansi_escape_bg
        fg_color = self.foreground.ansi_escape
        return f"{bg_color}{fg_color}{text}{ANSI_RESET}"

    def difference(self, other: 'Color') -> 'Color':
        return Color(
            abs(self.r - other.r),
            abs(self.g - other.g),
            abs(self.b - other.b),
        )

# endregion
# region Internal functions

# endregion Internal functions

# region Private functions

def _clamp(value: int, min_value: int = 0, max_value: int = 255) -> int:
    return max(min_value, min(max_value, value))


def _redistribute_rgb(r: float, g: float, b: float, a: float = 255) -> tuple[int, ...]:
    threshold = 255.999
    m = max(r, g, b)
    if m <= threshold:
        return int(r), int(g), int(b)
    total = r + g + b
    if total >= 3 * threshold:
        return int(threshold), int(threshold), int(threshold)
    x = (3 * threshold - total) / (3 * m - total)
    gray = threshold - x * m
    if a == 255:
        return int(gray + x * r), int(gray + x * g), int(gray + x * b)
    return int(gray + x * r), int(gray + x * g), int(gray + x * b), int(a)

def _rgba_from_name(color_name: str) -> tuple[int, ...]:
    """Retrieve a color by its human-readable name."""
    name = color_name.lower()
    for color_list in color_lists:
        if color_name in color_list:
            return color_list[color_name]

    if name == "transparent":
        return transparent

    raise ColorNotFoundError(color_name)


def _rgba_from_hex(hex_str: str) -> tuple[int, ...]:
    """Convert a hex color string to an RGBA tuple."""
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 6:  # RGB format
        r, g, b = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
        return r, g, b
    if len(hex_str) == 8:  # RGBA format
        r, g, b, a = (
            int(hex_str[0:2], 16),
            int(hex_str[2:4], 16),
            int(hex_str[4:6], 16),
            int(hex_str[6:8], 16),
        )
        return r, g, b, a
    if len(hex_str) == 3:  # CSS Short format
        r, g, b = (
            int(hex_str[0:1] * 2, 16),
            int(hex_str[1:2] * 2, 16),
            int(hex_str[2:3] * 2, 16),
        )
        return r, g, b
    raise ValueError()


# endregion Private functions


# region Public static functions

def name_lookup(color_to_name: Color) -> str:
    """Looks up a human-readable name for a Color using the color.pizza API.

    Makes a request to the color.pizza API to find the closest named color match
    for the given RGB values.

    Args:
        color_to_name: The Color object to find a name for

    Returns:
        str: The suggested name for the color from the API, or "unknown" if the
            API request fails

    Example:
        >>> new_color = painto.random_color()
        >>> print(painto.name_lookup(new_color))

    Raises:
        ImportError: If the requests library is not installed
    """
    # late import so we don't try unless we're actually going to use it.
    try:
        import requests
    except ImportError as e:
        raise RequestsRequiredError() from e

    url = "https://api.color.pizza/v1/"

    hex_color = f"{color_to_name.r:02X}{color_to_name.g:02X}{color_to_name.b:02X}"
    response = requests.get(f"{url}?values={hex_color}", timeout=5)
    if response.status_code == 200:
        api_data = response.json()
        suggested_name = api_data["colors"][0]["name"] if api_data["colors"] else "Unknown"
    else:
        suggested_name = "unknown"

    return suggested_name



def random_color(count: int = 1) -> Color | list[Color]:
    """Generates random color(s) with RGB values between 0-255.

    Args:
        count (int, optional): Number of random colors to generate. Defaults to 1.

    Returns:
        Color: If count=1, returns a single random Color object.
        list[Color]: If count>1, returns a list of random Color objects.

    Example:
        >>> color = painto.random_color()  # Get a single random color
        >>> colors = painto.random_color(5)  # Get 5 random colors

    If you're wanting a random color or colors from a specific color list,
    see ```ColorList.random()```.
    """
    if count == 1:
        return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # noqa: S311

    colors = []
    for _ in range(count):
        colors.append(Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))  # noqa: S311
    return colors

def color_range(start: Color,
                end: Color,
                steps: int = 10,
                *,
                inclusive: bool = False) -> Iterator[Color]:
    if steps < 0:
        raise ColorRangeError(steps)
    if inclusive:
        steps -= 1
    h_step = (end.h - start.h) / steps
    v_step = (end.v - start.v) / steps
    s_step = (end.s - start.s) / steps
    alpha_step = (end.a - start.a) / steps

    for i in range(steps):
        h = start.h + i * h_step
        v = start.v + i * v_step
        s = start.s + i * s_step
        a = start.a + i * alpha_step
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        yield Color(int(r), int(g), int(b), int(a))

    if inclusive:
        yield end

def sort_by_hue() -> None:
    """Sets the global color sorting method to sort by hue.

    This function changes the global sorting option to sort colors by their hue
    (rainbow) order. The default is to sort by luminosity/brightness. To change
    back to sorting by luminosity, call ```sort_by_luminosity()```.

    Returns:
        None
    """
    global SORT_BY
    SORT_BY = ColorSort.HUE

def sort_by_luminosity() -> None:
    """Sets the global color sorting method to sort by luminosity/brightness.

    This function changes the global sorting option to sort colors by their
    luminosity value. This is the default sorting method.

    You can change to sort by hue (rainbow) by calling ```sort_by_hue()```.

    Returns:
        None
    """
    global SORT_BY
    SORT_BY = ColorSort.LUMINOSITY

def sorting_by() -> str:
    """Gets the current global color sorting method.

    Returns:
        str: The name of the current sorting method ('hue' or 'luminosity')
    """
    return SORT_BY.name.lower()

def dynamic_name_lookup(lookup: bool = False) -> None:
    """Sets whether dynamic name lookup is enabled.

    When dynamic name lookup is enabled, if a color's name isn't known when
    using color.name, it will be looked up using the color.pizza API. With this
    disabled (the default), the name will return as the hex value. This uses
    the ```name_lookup()``` function and will raise an ImportError if the
    requests library is not installed.

    Note:
        Use this with care. It will slow any access to color.name that isn't known
        and cached.

    Args:
        lookup (bool, optional): Whether to enable dynamic name lookup. Defaults to False.

    Returns:
        None

    Example:
        >>> new_color = painto.Color("#946A87")
        >>> print(new_color.name)  # '#946A87'
        >>> painto.dynamic_name_lookup(True)
        >>> print(new_color.name)  # 'Fruit of Passion'
    """
    global DYNAMIC_NAME_LOOKUP
    DYNAMIC_NAME_LOOKUP = lookup

def dynamic_name_lookup_enabled() -> bool:
    """Returns whether dynamic name lookup is currently enabled. Change this
    with ```dynamic_name_lookup()```.

    Returns:
        bool: True if dynamic name lookup is enabled, False otherwise.
    """
    return DYNAMIC_NAME_LOOKUP

# endregion public static functions

# Add attributes to the class to make color names accessible as attributes


color_lists: list[dict[str, Color]] = []
transparent = Color(0, 0, 0, 0, name="transparent")


