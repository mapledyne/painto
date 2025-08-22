import os
import sys
import unittest

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import painto
from painto.color_list import ColorList


class TestColorList(unittest.TestCase):
    """Test cases for the ColorList class."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.test_colors = ColorList({
            "red": painto.Color("#ff0000", name="red", source="test"),
            "green": painto.Color("#00ff00", name="green", source="test"),
            "blue": painto.Color("#0000ff", name="blue", source="test"),
            "yellow": painto.Color("#ffff00", name="yellow", source="test"),
            "purple": painto.Color("#800080", name="purple", source="test"),
        })

    def test_color_list_creation(self) -> None:
        """Test creating a ColorList with colors."""
        self.assertIsInstance(self.test_colors, ColorList)
        self.assertEqual(len(self.test_colors), 5)
        self.assertIn("red", self.test_colors)
        self.assertIn("green", self.test_colors)

    def test_color_list_dict_access(self) -> None:
        """Test accessing colors using dictionary syntax."""
        red = self.test_colors["red"]
        self.assertIsInstance(red, painto.Color)
        self.assertEqual(red.hex.upper(), "#FF0000")
        self.assertEqual(red.name, "red")
        self.assertEqual(red.source, "test")

    def test_color_list_attribute_access(self) -> None:
        """Test accessing colors using attribute syntax."""
        red = self.test_colors.red
        green = self.test_colors.green
        self.assertIsInstance(red, painto.Color)
        self.assertIsInstance(green, painto.Color)
        self.assertEqual(red.hex.upper(), "#FF0000")
        self.assertEqual(green.hex.upper(), "#00FF00")

    def test_color_list_iteration(self) -> None:
        """Test iterating over ColorList."""
        colors = list(self.test_colors.values())
        self.assertEqual(len(colors), 5)
        for color in colors:
            self.assertIsInstance(color, painto.Color)

    def test_color_list_keys(self) -> None:
        """Test getting keys from ColorList."""
        keys = list(self.test_colors.keys())
        expected_keys = ["red", "green", "blue", "yellow", "purple"]
        self.assertEqual(set(keys), set(expected_keys))

    def test_color_list_items(self) -> None:
        """Test getting items from ColorList."""
        items = list(self.test_colors.items())
        self.assertEqual(len(items), 5)
        for name, color in items:
            self.assertIsInstance(name, str)
            self.assertIsInstance(color, painto.Color)
            self.assertEqual(color.name, name)

    def test_color_list_contains(self) -> None:
        """Test checking if colors exist in ColorList."""
        self.assertIn("red", self.test_colors)
        self.assertIn("green", self.test_colors)
        self.assertNotIn("nonexistent", self.test_colors)

    def test_color_list_get(self) -> None:
        """Test using get() method on ColorList."""
        red = self.test_colors.get("red")
        self.assertIsInstance(red, painto.Color)
        self.assertEqual(red.hex.upper(), "#FF0000")

        # Test with default value
        default_color = self.test_colors.get("nonexistent", painto.Color("#000000"))
        self.assertIsInstance(default_color, painto.Color)
        self.assertEqual(default_color.hex.upper(), "#000000")

    def test_color_list_pop(self) -> None:
        """Test removing colors from ColorList."""
        color_list = ColorList(self.test_colors)
        red = color_list.pop("red")
        self.assertIsInstance(red, painto.Color)
        self.assertEqual(red.hex.upper(), "#FF0000")
        self.assertNotIn("red", color_list)
        self.assertEqual(len(color_list), 4)

    def test_color_list_update(self) -> None:
        """Test updating ColorList with new colors."""
        color_list = ColorList(self.test_colors)
        new_colors = {
            "cyan": painto.Color("#00ffff", name="cyan", source="test"),
            "magenta": painto.Color("#ff00ff", name="magenta", source="test"),
        }
        color_list.update(new_colors)
        self.assertEqual(len(color_list), 7)
        self.assertIn("cyan", color_list)
        self.assertIn("magenta", color_list)


class TestColorListRandom(unittest.TestCase):
    """Test cases for ColorList random functionality."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.test_colors = ColorList({
            "red": painto.Color("#ff0000", name="red", source="test"),
            "green": painto.Color("#00ff00", name="green", source="test"),
            "blue": painto.Color("#0000ff", name="blue", source="test"),
            "yellow": painto.Color("#ffff00", name="yellow", source="test"),
            "purple": painto.Color("#800080", name="purple", source="test"),
        })

    def test_random_single_color(self) -> None:
        """Test getting a single random color."""
        random_color = self.test_colors.random()
        self.assertIsInstance(random_color, painto.Color)
        self.assertIn(random_color, self.test_colors.values())

    def test_random_multiple_colors(self) -> None:
        """Test getting multiple random colors."""
        random_colors = self.test_colors.random(3)
        self.assertIsInstance(random_colors, list)
        self.assertEqual(len(random_colors), 3)
        for color in random_colors:
            self.assertIsInstance(color, painto.Color)
            self.assertIn(color, self.test_colors.values())

    def test_random_all_colors(self) -> None:
        """Test getting all colors randomly."""
        random_colors = self.test_colors.random(5)
        self.assertIsInstance(random_colors, list)
        self.assertEqual(len(random_colors), 5)
        # All colors should be unique
        self.assertEqual(len(set(random_colors)), 5)

    def test_random_count_validation(self) -> None:
        """Test that random() validates count properly."""
        # Should work with count equal to available colors
        colors = self.test_colors.random(5)
        self.assertEqual(len(colors), 5)

        # Should raise ValueError for count > available colors
        with self.assertRaises(ValueError):
            self.test_colors.random(10)

    def test_random_empty_list(self) -> None:
        """Test random() with empty ColorList."""
        empty_list = ColorList()
        with self.assertRaises(IndexError):
            empty_list.random()


class TestColorListBuiltInCollections(unittest.TestCase):
    """Test cases for built-in color collections."""

    def test_w3c_collection(self) -> None:
        """Test W3C color collection."""
        self.assertIsInstance(painto.w3c, ColorList)
        self.assertGreater(len(painto.w3c), 0)

        # Test some known W3C colors
        if "red" in painto.w3c:
            red = painto.w3c["red"]
            self.assertIsInstance(red, painto.Color)
            self.assertEqual(red.source, "w3c")

    def test_xkcd_collection(self) -> None:
        """Test XKCD color collection."""
        self.assertIsInstance(painto.xkcd, ColorList)
        self.assertGreater(len(painto.xkcd), 0)

        # Test some known XKCD colors
        if "red" in painto.xkcd:
            red = painto.xkcd["red"]
            self.assertIsInstance(red, painto.Color)
            self.assertEqual(red.source, "xkcd")

    def test_pride_collection(self) -> None:
        """Test Pride color collection."""
        self.assertIsInstance(painto.pride, ColorList)
        self.assertGreater(len(painto.pride), 0)

        # Test some known Pride colors
        if "red" in painto.pride:
            red = painto.pride["red"]
            self.assertIsInstance(red, painto.Color)
            self.assertEqual(red.source, "pride")

    def test_base_colors_collection(self) -> None:
        """Test base colors collection."""
        self.assertIsInstance(painto.base_colors, ColorList)
        self.assertGreater(len(painto.base_colors), 0)

    def test_collection_sources(self) -> None:
        """Test that colors have correct source attributes."""
        collections = [painto.w3c, painto.xkcd, painto.pride, painto.base_colors]
        sources = ["w3c", "xkcd", "pride", "base"]

        for collection, expected_source in zip(collections, sources, strict=False):
            if len(collection) > 0:
                # Get first color from collection
                first_color = next(iter(collection.values()))
                self.assertEqual(first_color.source, expected_source)


class TestColorListIntegration(unittest.TestCase):
    """Test cases for ColorList integration with other painto features."""

    def test_color_list_with_color_range(self) -> None:
        """Test using ColorList colors with color_range function."""
        colors = ColorList({
            "start": painto.Color("#ff0000"),
            "end": painto.Color("#0000ff"),
        })

        gradient = list(painto.color_range(colors["start"], colors["end"], 3))
        self.assertEqual(len(gradient), 3)
        for color in gradient:
            self.assertIsInstance(color, painto.Color)

    def test_color_list_with_arithmetic(self) -> None:
        """Test using ColorList colors with arithmetic operations."""
        colors = ColorList({
            "red": painto.Color("#ff0000"),
            "blue": painto.Color("#0000ff"),
        })

        purple = colors["red"] + colors["blue"]
        self.assertIsInstance(purple, painto.Color)

        darker_red = colors["red"] / 2
        self.assertIsInstance(darker_red, painto.Color)

    def test_color_list_with_console_output(self) -> None:
        """Test using ColorList colors with console output methods."""
        colors = ColorList({
            "red": painto.Color("#ff0000"),
            "green": painto.Color("#00ff00"),
        })

        red = colors.red
        red_text = red.console("Red text")
        self.assertIsInstance(red_text, str)
        self.assertIn("Red text", red_text)
        self.assertIn(red.ansi_escape, red_text)
        self.assertIn(red.ansi_reset, red_text)

        green = colors.green
        green_bg = green.console_bg("Green background")
        self.assertIsInstance(green_bg, str)
        self.assertIn("Green background", green_bg)
        self.assertIn(green.ansi_escape_bg, green_bg)
        self.assertIn(green.foreground.ansi_escape, green_bg)
        self.assertIn(green.ansi_reset, green_bg)


if __name__ == '__main__':
    unittest.main(verbosity=2)
