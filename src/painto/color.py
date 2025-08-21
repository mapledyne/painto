import warnings
from typing import Tuple, Union
import colorsys
import random
from enum import Enum, auto



try:
    # Suppress deprecation warnings from external dependencies
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="pygame")
    import pygame
    _HAS_PYGAME = True
except ImportError:
    _HAS_PYGAME = False

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
# region === INITIALIZATION ===

    def __new__(cls, value: Union[str, int, Tuple[int, ...]], g: int = -1, b: int = -1, a: int = 255, name: str = '', source: str = ''):
        return super().__new__(cls, (value, g, b, a))


    def __init__(self, *args, **kwargs):
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
        if len(args) == 1:
            value = args[0]
            if isinstance(value, str):
                if value.startswith("#"):  # Handle hex string
                    r, g, b, a = _rgba_from_hex(value)
                else:  # Handle color name
                    r, g, b, a = _rgba_from_name(value)
            elif isinstance(value, tuple) and len(value) == 3:  # Handle RGB tuple
                r, g, b = value
                a = 255
            elif isinstance(value, tuple) and len(value) == 4:  # Handle RGBA tuple
                r, g, b, a = value
            else:
                raise ValueError("Single argument must be a color name, hex string, or RGB(A) tuple")
        elif len(args) in {3, 4}:  # Handle r,g,b[,a] values
            r, g, b, a = args if len(args) == 4 else (*args, 255)
        else:
            raise ValueError("Invalid arguments. Must be a color name, hex string, RGB(A) tuple, or 3-4 RGB(A) values")

        self._r = int(r)
        self._g = int(g)
        self._b = int(b)
        self._a = int(a)

        if 'name' in kwargs:
            self._name = kwargs['name']
        if 'source' in kwargs:
            self._source = kwargs['source']
        if "escape" in kwargs:
            self._escape = kwargs['escape']

# endregion
# region === DUNDER FUNCTIONS ===

    def __repr__(self) -> str:
        return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})"

    def __str__(self) -> str:
        return self.name

    def __add__(self, other) -> 'Color':
        """Blend two colors by averaging their RGBA values."""
        if not isinstance(other, Color):
            raise TypeError("Can only add another Color instance.")
        r = (self.r + other.r) // 2
        g = (self.g + other.g) // 2
        b = (self.b + other.b) // 2
        a = (self.a + other.a) // 2
        return Color(r, g, b, a)

    def __eq__(self, other) -> bool:
        """Compare two colors for equality."""
        if isinstance(other, Color):
            return self.rgba == other.rgba
        if isinstance(other, str):
            if other.lower() in [self.name, self.hex]:
                return True
            return False
        if isinstance(other, tuple):
            if len(other) == 3:
                return self.rgba == (other[0], other[1], other[2], 255)
            elif len(other) == 4:
                return self.rgba == other
            else:
                return False
        return NotImplemented

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __mul__(self, other) -> 'Color':
        """Multiply the color by a factor (will lighten/darken the color)."""
        if isinstance(other, (int, float)):

            r = int(self.r * other)
            g = int(self.g * other)
            b = int(self.b * other)

            return _redistribute_rgb(r, g, b)

        return NotImplemented

    def __rmul__(self, other) -> 'Color':
        return self * other

    def __truediv__(self, factor) -> 'Color':
        return self * (1 / factor)

    def __hash__(self) -> int:
        return hash(self.rgba)

    # Compare colors by brightness
    def __lt__(self, other: 'Color') -> bool:
        if SORT_BY == ColorSort.HUE:
            return self.h < other.h
        if SORT_BY == ColorSort.LUMINOSITY:
            return self.luminosity < other.luminosity

    def __le__(self, other: 'Color') -> bool:
        if SORT_BY == ColorSort.HUE:
            return self.h <= other.h
        if SORT_BY == ColorSort.LUMINOSITY:
            return self.luminosity <= other.luminosity

    def __gt__(self, other: 'Color') -> bool:
        if SORT_BY == ColorSort.HUE:
            return self.h > other.h
        if SORT_BY == ColorSort.LUMINOSITY:
            return self.luminosity > other.luminosity

    def __ge__(self, other: 'Color') -> bool:
        if SORT_BY == ColorSort.HUE:
            return self.h >= other.h
        if SORT_BY == ColorSort.LUMINOSITY:
            return self.luminosity >= other.luminosity

    def __neg__(self) -> 'Color':
        return self.difference(Color(255, 255, 255))

    def __bool__(self) -> bool:
        return self.a > 0

    def __len__(self) -> int:
        if self.a == 255:
            return 3
        return 4

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.r
        elif index == 1:
            return self.g
        elif index == 2:
            return self.b
        elif index == 3:
            return self.a

        raise IndexError("index out of range")

    def __setitem__(self, index: int, value: int):
        if index == 0:
            self.r = value
        elif index == 1:
            self.g = value
        elif index == 2:
            self.b = value
        elif index == 3:
            self.a = value
        raise IndexError("index out of range")

    def __iter__(self):
        if self.a == 255:
            return iter(self.rgb)
        return iter(self.rgba)

    def __int__(self) -> int:
        return (self.r << 16) + (self.g << 8) + self.b

# endregion
# region === PUBLIC PROPERTIES ===

    @property
    def rgba(self) -> Tuple[int, int, int, int]:
        return self.r, self.g, self.b, self.a


    @property
    def r(self) -> int:
        return self._r

    @property
    def g(self) -> int:
        return self._g

    @property
    def b(self) -> int:
        return self._b

    @property
    def a(self) -> int:
        return self._a

    @property
    def rgb(self) -> Tuple[int, int, int]:
        return self.r, self.g, self.b

    @property
    def hsv(self) -> Tuple[float, float, float]:
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
            self._hex = f"#{self.r:02x}{self.g:02x}{self.b:02x}" + (f"{self.a:02x}" if self.a != 255 else "")
        return self._hex

    @property
    def name(self) -> str:
        """Return the friendly name if it exists, otherwise the hex value."""
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
    def console(self) -> str:
        if not hasattr(self, "_console"):
            self._console = f"\033[38;2;{self.r};{self.g};{self.b}m"
        return self._console
    
    @property
    def console_bg(self) -> str:
        if not hasattr(self, "_console_bg"):
            self._console_bg = f"\033[48;2;{self.r};{self.g};{self.b}m"
        return self._console_bg


# endregion
# region === PUBLIC FUNCTIONS ====
    def to_pygame(self):
        if not _HAS_PYGAME:
            raise ImportError("pygame is required to use to_pygame()")
        return pygame.Color(*self.rgba)
    
    def console_string(self, text: str):
        fg_color = self.console
        return f"{fg_color}{text}{ANSI_RESET}"
    
    def console_string_bg(self, text: str):
        bg_color = self.console_bg
        fg_color = self.foreground.console
        return f"{bg_color}{fg_color}{text}{ANSI_RESET}"

    # convenient aliases, but not really required.
    def lighten(self, factor: float = 1.2) -> 'Color':
        """Lighten the color."""
        return self * factor

    def darken(self, factor: float = 0.8) -> 'Color':
        """Darken the color."""
        return self * factor

    def semi_transparent(self, alpha: int = 128) -> 'Color':
        return Color((self.r, self.g, self.b, alpha))

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


def _redistribute_rgb(r: float, g: float, b: float) -> Color:
    threshold = 255.999
    m = max(r, g, b)
    if m <= threshold:
        return Color(int(r), int(g), int(b))
    total = r + g + b
    if total >= 3 * threshold:
        return Color(int(threshold), int(threshold), int(threshold))
    x = (3 * threshold - total) / (3 * m - total)
    gray = threshold - x * m
    return Color(int(gray + x * r), int(gray + x * g), int(gray + x * b))


# endregion Private functions


# region Public static functions


def name_lookup(color_to_name: Color) -> str:
    # Return a list of colors used this session

    # late import so we don't try unless we're actually going to use it.
    try:
        import requests
    except ImportError:
        raise ImportError("requests is required to use name_lookup()")

    url = "https://api.color.pizza/v1/"

    hex_color = f"{color_to_name.r:02X}{color_to_name.g:02X}{color_to_name.b:02X}"
    response = requests.get(f"{url}?values={hex_color}", timeout=5)
    if response.status_code == 200:
        api_data = response.json()
        suggested_name = api_data["colors"][0]["name"] if api_data["colors"] else "Unknown"
    else:
        suggested_name = "unknown"

    return suggested_name


def _rgba_from_name(color_name: str) -> tuple[int, ...]:
    """Retrieve a color by its human-readable name."""
    name = color_name.lower()
    for color_list in color_lists:
        if color_name in color_list:
            return color_list[color_name]

    if name == "transparent":
        return transparent

    raise ValueError(f"Color '{color_name}' not found in predefined color sets.")


def _rgba_from_hex(hex_str: str) -> Tuple[int, int, int, int]:
    """Convert a hex color string to an RGBA tuple."""
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 6:  # RGB format
        r, g, b = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
        return r, g, b, 255
    elif len(hex_str) == 8:  # RGBA format
        r, g, b, a = (
            int(hex_str[0:2], 16),
            int(hex_str[2:4], 16),
            int(hex_str[4:6], 16),
            int(hex_str[6:8], 16),
        )
        return r, g, b, a
    elif len(hex_str) == 3:  # CSS Short format
        r, g, b = (
            int(hex_str[0:1] * 2, 16),
            int(hex_str[1:2] * 2, 16),
            int(hex_str[2:3] * 2, 16),
        )
        return r, g, b, 255
    raise ValueError("Invalid hex string. Must be in the format #RRGGBB or #RRGGBBAA. CSS Short also supported (#aaa)")

def random_color(count: int = 1) -> Color | list[Color]:
    if count == 1:
        return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return [Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(count)]

def color_range(start: Color, end: Color, steps: int = 10, inclusive: bool = False) -> list[Color]:
    if steps < 0:
        raise ValueError("steps must be greater than 0")
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
        yield Color(r, g, b, a)

    if inclusive:
        yield end

def sort_by_hue():
    global SORT_BY
    SORT_BY = ColorSort.HUE

def sort_by_luminosity():
    global SORT_BY
    SORT_BY = ColorSort.LUMINOSITY

def sorting_by() -> str:
    return SORT_BY.name.lower()

def dynamic_name_lookup(lookup: bool = False):
    global DYNAMIC_NAME_LOOKUP
    DYNAMIC_NAME_LOOKUP = lookup

def dynamic_name_lookup_enabled() -> bool:
    return DYNAMIC_NAME_LOOKUP

# endregion public static functions

# Add attributes to the class to make color names accessible as attributes


color_lists: list[dict[str, Color]] = []
transparent = Color(0, 0, 0, 0, name="transparent")


