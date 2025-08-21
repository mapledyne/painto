import unittest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import painto

class TestColor(unittest.TestCase):
    """Test cases for the Color class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.red = painto.red
        self.blue = painto.blue
        self.green = painto.green
    
    def test_color_creation_from_name(self):
        """Test creating colors from color names."""
        self.assertIsInstance(self.red, painto.Color)
        self.assertIsInstance(self.blue, painto.Color)
        self.assertIsInstance(self.green, painto.Color)
    
    def test_color_creation_from_hex(self):
        """Test creating colors from hex strings."""
        red_hex = painto.Color("#FF0000")
        blue_hex = painto.Color("#0000ff")
        hex_css_short = painto.Color("#aaa")
        self.assertIsInstance(red_hex, painto.Color)
        self.assertIsInstance(blue_hex, painto.Color)
        self.assertIsInstance(hex_css_short, painto.Color)
    
    def test_color_creation_from_rgb(self):
        """Test creating colors from RGB values."""
        red_rgb = painto.Color(255, 0, 0)
        blue_rgb = painto.Color(0, 0, 255)
        self.assertIsInstance(red_rgb, painto.Color)
        self.assertIsInstance(blue_rgb, painto.Color)
    
    def test_color_properties(self):
        """Test basic color properties."""
        self.assertEqual(self.red.r, 255)
        self.assertEqual(self.red.g, 0)
        self.assertEqual(self.red.b, 0)
        self.assertEqual(self.red.a, 255)
    
    def test_color_hex_property(self):
        """Test hex property."""
        self.assertEqual(self.red.hex, "#ff0000")
        self.assertEqual(self.blue.hex, "#0000ff")
    
    def test_transparent_color(self):
        """Test transparent color."""
        self.assertEqual(painto.transparent.a, 0)
    
    def test_color_arithmetic(self):
        """Test color arithmetic operations."""
        purple = self.red + self.blue
        self.assertIsInstance(purple, painto.Color)
        
        darker_red = self.red / 2
        self.assertIsInstance(darker_red, painto.Color)


class TestColorLists(unittest.TestCase):
    """Test cases for color lists."""
    
    def test_color_lists_exist(self):
        """Test that color lists are accessible."""
        self.assertIsNotNone(painto.w3c)
        self.assertIsNotNone(painto.xkcd)
        self.assertIsNotNone(painto.pride)
        self.assertIsNotNone(painto.base_colors)

    def test_color_list_access(self):
        """Test accessing colors from lists."""
        # Test accessing a known color from w3c
        if "red" in painto.w3c:
            red_from_w3c = painto.w3c["red"]
            self.assertIsInstance(red_from_w3c, painto.Color)
    
    def test_pride_colors(self):
        """Test pride color list."""
        if "blue" in painto.pride and "red" in painto.pride:
            pride_blue = painto.pride.blue
            pride_red = painto.pride.red
            self.assertIsInstance(pride_blue, painto.Color)
            self.assertIsInstance(pride_red, painto.Color)


class TestColorFunctions(unittest.TestCase):
    """Test cases for color utility functions."""
    
    def test_color_range(self):
        """Test color_range function."""
        red = painto.red
        blue = painto.blue

        colors = list(painto.color_range(red, blue, 5))
        self.assertEqual(len(colors), 5)
        self.assertIsInstance(colors[0], painto.Color)
        self.assertIsInstance(colors[-1], painto.Color)
        self.assertEqual(colors[0], red)
        self.assertNotEqual(colors[-1], blue)
    
    def test_color_range_inclusive(self):
        """Test color_range with inclusive=True."""
        red = painto.red
        blue = painto.blue
        
        colors = list(painto.color_range(red, blue, 3, inclusive=True))
        self.assertEqual(len(colors), 3)
        self.assertIsInstance(colors[0], painto.Color)
        self.assertIsInstance(colors[-1], painto.Color)
        self.assertEqual(colors[0], red)
        self.assertEqual(colors[-1], blue)


if __name__ == '__main__':
    # Run tests using unittest.main()
    unittest.main(verbosity=2)
