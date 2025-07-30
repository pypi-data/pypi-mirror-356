"""Unit tests for validation utilities."""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import json

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dolze_templates.exceptions import ValidationError, ResourceError
from dolze_templates.utils.validation import (
    validate_type,
    validate_range,
    validate_choice,
    validate_color,
    validate_position,
    validate_size,
    validate_font_path,
    validate_url,
    validate_component,
    validate_template_config,
    validate_text_component,
    validate_image_component,
    validate_shape_component,
    MIN_FONT_SIZE,
    MAX_FONT_SIZE,
    VALID_FONT_WEIGHTS,
    VALID_TEXT_ALIGNS,
    VALID_BORDER_STYLES,
    VALID_EFFECTS,
    MIN_IMAGE_DIMENSION,
    MAX_IMAGE_DIMENSION,
    MIN_BLUR_RADIUS,
    MAX_BLUR_RADIUS,
)


class TestValidationUtils(unittest.TestCase):
    """Test validation utility functions."""

    def test_validate_type_valid(self):
        """Test validate_type with valid input."""
        self.assertEqual(validate_type(42, int, "test"), 42)
        self.assertEqual(validate_type("test", str, "test"), "test")
        self.assertEqual(validate_type(3.14, (int, float), "test"), 3.14)
        self.assertEqual(validate_type(True, bool, "test"), True)
        self.assertEqual(validate_type(None, type(None), "test"), None)

    def test_validate_type_invalid(self):
        """Test validate_type with invalid input."""
        with self.assertRaises(ValidationError) as cm:
            validate_type("not an int", int, "test")
        self.assertIn("must be of type int", str(cm.exception))

        with self.assertRaises(ValidationError) as cm:
            validate_type(42, str, "test")
        self.assertIn("must be of type str", str(cm.exception))

        with self.assertRaises(ValidationError) as cm:
            validate_type(None, int, "test", allow_none=False)
        self.assertIn("must be of type int", str(cm.exception))

    def test_validate_range_valid(self):
        """Test validate_range with valid input."""
        self.assertEqual(validate_range(5, 0, 10, "test"), 5)
        self.assertEqual(validate_range(0, 0, 10, "test"), 0)
        self.assertEqual(validate_range(10, 0, 10, "test"), 10)
        self.assertEqual(validate_range(5.5, 0.0, 10.0, "test"), 5.5)
        self.assertEqual(validate_range(-5, -10, 10, "test"), -5)

    def test_validate_range_invalid(self):
        """Test validate_range with invalid input."""
        with self.assertRaises(ValidationError) as cm:
            validate_range(15, 0, 10, "test")
        self.assertIn("must be between 0 and 10", str(cm.exception))

        with self.assertRaises(ValidationError) as cm:
            validate_range(-1, 0, 10, "test")
        self.assertIn("must be between 0 and 10", str(cm.exception))

        with self.assertRaises(ValidationError) as cm:
            validate_range("not a number", 0, 10, "test")
        self.assertIn("must be a number", str(cm.exception))

    def test_validate_choice_valid(self):
        """Test validate_choice with valid input."""
        choices = ["a", "b", "c"]
        self.assertEqual(validate_choice("a", choices, "test"), "a")
        self.assertEqual(validate_choice("b", choices, "test"), "b")
        self.assertEqual(validate_choice("c", choices, "test"), "c")
        self.assertEqual(validate_choice(None, choices, "test", allow_none=True), None)

    def test_validate_choice_invalid(self):
        """Test validate_choice with invalid input."""
        choices = ["a", "b", "c"]
        with self.assertRaises(ValidationError) as cm:
            validate_choice("d", choices, "test")
        self.assertIn("must be one of", str(cm.exception))

        with self.assertRaises(ValidationError) as cm:
            validate_choice(123, choices, "test")
        self.assertIn("must be one of", str(cm.exception))

        with self.assertRaises(ValidationError) as cm:
            validate_choice(None, choices, "test", allow_none=False)
        self.assertIn("must be one of", str(cm.exception))

    def test_validate_color_valid(self):
        """Test validate_color with valid input."""
        # Test hex colors
        self.assertEqual(validate_color("#ff0000", "test"), (255, 0, 0, 255))
        self.assertEqual(validate_color("#00ff00", "test"), (0, 255, 0, 255))
        self.assertEqual(validate_color("#0000ff", "test"), (0, 0, 255, 255))
        self.assertEqual(
            validate_color("#ff000080", "test"), (255, 0, 0, 128)
        )  # With alpha
        self.assertEqual(validate_color("#f00", "test"), (255, 0, 0, 255))  # Short hex
        self.assertEqual(
            validate_color("#f008", "test"), (255, 0, 0, 136)
        )  # Short hex with alpha

        # Test RGB tuples
        self.assertEqual(validate_color((255, 0, 0), "test"), (255, 0, 0, 255))
        self.assertEqual(validate_color([0, 255, 0], "test"), (0, 255, 0, 255))

        # Test RGBA tuples
        self.assertEqual(validate_color((255, 0, 0, 128), "test"), (255, 0, 0, 128))
        self.assertEqual(validate_color([0, 255, 0, 64], "test"), (0, 255, 0, 64))

        # Test None
        self.assertEqual(validate_color(None, "test"), (0, 0, 0, 0))  # Transparent

        # Test with alpha=False
        self.assertEqual(
            validate_color((255, 0, 0), "test", alpha=False), (255, 0, 0, 255)
        )

    def test_validate_color_invalid(self):
        """Test validate_color with invalid input."""
        # Invalid hex
        with self.assertRaises(ValidationError) as cm:
            validate_color("not a color", "test")
        self.assertIn("Invalid color format", str(cm.exception))

        # Invalid hex format
        with self.assertRaises(ValidationError) as cm:
            validate_color("#zzz", "test")
        self.assertIn("Invalid color format", str(cm.exception))

        # Invalid RGB values
        with self.assertRaises(ValidationError) as cm:
            validate_color((300, 0, 0), "test")
        self.assertIn("Color values must be between 0 and 255", str(cm.exception))

        with self.assertRaises(ValidationError) as cm:
            validate_color((0, -1, 0), "test")
        self.assertIn("Color values must be between 0 and 255", str(cm.exception))

        # Invalid alpha
        with self.assertRaises(ValidationError) as cm:
            validate_color((0, 0, 255, 300), "test")
        self.assertIn("Alpha value must be between 0 and 255", str(cm.exception))

        # Invalid type
        with self.assertRaises(ValidationError) as cm:
            validate_color(12345, "test")
        self.assertIn(
            "Color must be a hex string or RGBA tuple/list", str(cm.exception)
        )

        # Invalid sequence length
        with self.assertRaises(ValidationError) as cm:
            validate_color((1, 2), "test")
        self.assertIn("Color must have 3 or 4 values", str(cm.exception))

        with self.assertRaises(ValidationError) as cm:
            validate_color((1, 2, 3, 4, 5), "test")
        self.assertIn("Color must have 3 or 4 values", str(cm.exception))

    def test_validate_position_valid(self):
        """Test validate_position with valid input."""
        # Test with dict
        position = {"x": 10, "y": 20}
        self.assertEqual(validate_position(position, "test"), (10, 20))

        # Test with dict with string numbers
        position_str = {"x": "10", "y": "20"}
        self.assertEqual(validate_position(position_str, "test"), (10, 20))

        # Test with tuple
        self.assertEqual(validate_position((30, 40), "test"), (30, 40))

        # Test with list
        self.assertEqual(validate_position([50, 60], "test"), (50, 60))

        # Test with float values (should be converted to int)
        self.assertEqual(validate_position((10.5, 20.9), "test"), (10, 20))

        # Test with string values
        self.assertEqual(validate_position(("30", "40"), "test"), (30, 40))

    def test_validate_position_invalid(self):
        """Test validate_position with invalid input."""
        # Missing keys
        with self.assertRaises(ValidationError) as cm:
            validate_position({"x": 10}, "test")
        self.assertIn("must contain x and y coordinates", str(cm.exception))

        # Invalid type
        with self.assertRaises(ValidationError) as cm:
            validate_position("not a position", "test")
        self.assertIn(
            "must be a dict with x,y or a sequence of 2 numbers", str(cm.exception)
        )

        # Invalid sequence length
        with self.assertRaises(ValidationError) as cm:
            validate_position([10], "test")
        self.assertIn("must be a sequence of 2 numbers", str(cm.exception))

        with self.assertRaises(ValidationError) as cm:
            validate_position([10, 20, 30], "test")
        self.assertIn("must be a sequence of 2 numbers", str(cm.exception))

        # Non-numeric values
        with self.assertRaises(ValidationError) as cm:
            validate_position(["not", "numbers"], "test")
        self.assertIn("must contain numbers", str(cm.exception))

    def test_validate_size_valid(self):
        """Test validate_size with valid input."""
        # Test with dict
        size = {"width": 100, "height": 200}
        self.assertEqual(validate_size(size, "test"), (100, 200))

        # Test with dict with string numbers
        size_str = {"width": "100", "height": "200"}
        self.assertEqual(validate_size(size_str, "test"), (100, 200))

        # Test with tuple
        self.assertEqual(validate_size((300, 400), "test"), (300, 400))

        # Test with list
        self.assertEqual(validate_size([500, 600], "test"), (500, 600))

        # Test with float values (should be converted to int)
        self.assertEqual(validate_size((100.5, 200.9), "test"), (100, 200))

        # Test with string values
        self.assertEqual(validate_size(("300", "400"), "test"), (300, 400))

        # Test with min/max constraints
        self.assertEqual(
            validate_size((MIN_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION), "test"),
            (MIN_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION),
        )

    def test_validate_size_invalid(self):
        """Test validate_size with invalid input."""
        # Missing keys
        with self.assertRaises(ValidationError) as cm:
            validate_size({"width": 100}, "test")
        self.assertIn("must contain width and height", str(cm.exception))

        # Invalid type
        with self.assertRaises(ValidationError) as cm:
            validate_size("not a size", "test")
        self.assertIn(
            "must be a dict with width,height or a sequence of 2 numbers",
            str(cm.exception),
        )

        # Invalid sequence length
        with self.assertRaises(ValidationError) as cm:
            validate_size([100], "test")
        self.assertIn("must be a sequence of 2 numbers", str(cm.exception))

        with self.assertRaises(ValidationError) as cm:
            validate_size([100, 200, 300], "test")
        self.assertIn("must be a sequence of 2 numbers", str(cm.exception))

        # Non-numeric values
        with self.assertRaises(ValidationError) as cm:
            validate_size(["not", "numbers"], "test")
        self.assertIn("must contain numbers", str(cm.exception))

        # Invalid dimensions
        with self.assertRaises(ValidationError) as cm:
            validate_size([0, 100], "test")
        self.assertIn(
            f"width must be between {MIN_IMAGE_DIMENSION} and {MAX_IMAGE_DIMENSION}",
            str(cm.exception),
        )

        with self.assertRaises(ValidationError) as cm:
            validate_size([100, 0], "test")
        self.assertIn(
            f"height must be between {MIN_IMAGE_DIMENSION} and {MAX_IMAGE_DIMENSION}",
            str(cm.exception),
        )

        with self.assertRaises(ValidationError) as cm:
            validate_size([MAX_IMAGE_DIMENSION + 1, 100], "test")
        self.assertIn(
            f"width must be between {MIN_IMAGE_DIMENSION} and {MAX_IMAGE_DIMENSION}",
            str(cm.exception),
        )

        # Test with percentage
        size_dict_pct = {"width": "50%", "height": "100%"}
        self.assertEqual(
            validate_size(size_dict_pct, "test"),
            {"width": (50, "%"), "height": (100, "%")},
        )

    @patch("os.path.isfile")
    @patch("PIL.ImageFont.truetype")
    def test_validate_font_path_valid(self, mock_truetype, mock_isfile):
        """Test validate_font_path with valid font path."""
        mock_isfile.return_value = True
        mock_truetype.return_value = MagicMock()

        # Test with existing font file
        result = validate_font_path("/path/to/font.ttf")
        self.assertEqual(result, "/path/to/font.ttf")

        # Test with font name
        result = validate_font_path("Arial")
        self.assertEqual(result, "Arial")

    def test_validate_url_valid(self):
        """Test validate_url with valid URLs."""
        urls = [
            "https://example.com",
            "http://example.com/path?query=string",
            "https://sub.example.com:8080/path#fragment",
        ]
        for url in urls:
            self.assertEqual(validate_url(url, "test"), url)

    def test_validate_component_text(self):
        """Test validate_component with a text component."""
        component = {
            "type": "text",
            "text": "Hello, World!",
            "position": {"x": 10, "y": 20},
            "font_size": 24,
            "color": "#ff0000",
            "font_weight": "bold",
            "align": "center",
        }

        result = validate_component(component)
        self.assertEqual(result["type"], "text")
        self.assertEqual(result["text"], "Hello, World!")
        self.assertEqual(result["font_size"], 24)
        self.assertEqual(result["color"], (255, 0, 0, 255))
        self.assertEqual(result["font_weight"], "bold")
        self.assertEqual(result["align"], "center")

    def test_validate_component_image(self):
        """Test validate_component with an image component."""
        component = {
            "type": "image",
            "image_url": "https://example.com/image.jpg",
            "position": {"x": 0, "y": 0},
            "size": {"width": 100, "height": 100},
        }

        with patch(
            "dolze_templates.utils.validation.validate_url"
        ) as mock_validate_url:
            mock_validate_url.return_value = "https://example.com/image.jpg"
            result = validate_component(component)

        self.assertEqual(result["type"], "image")
        self.assertEqual(result["image_url"], "https://example.com/image.jpg")
        self.assertEqual(result["size"], {"width": 100, "height": 100})

    def test_validate_template_config_minimal(self):
        """Test validate_template_config with minimal valid config."""
        config = {
            "name": "Test Template",
            "components": [
                {"type": "text", "text": "Hello, World!", "position": {"x": 0, "y": 0}}
            ],
        }

        with patch(
            "dolze_templates.utils.validation.validate_component"
        ) as mock_validate_component:
            mock_validate_component.return_value = config["components"][0].copy()
            result = validate_template_config(config)

        self.assertEqual(result["name"], "Test Template")
        self.assertEqual(len(result["components"]), 1)
        self.assertEqual(result["components"][0]["type"], "text")

    def test_validate_template_config_full(self):
        """Test validate_template_config with all possible fields."""
        config = {
            "name": "Full Template",
            "size": {"width": 800, "height": 600},
            "background_color": "#ffffff",
            "use_base_image": False,
            "effects": {"blur": {"radius": 5}},
            "components": [
                {
                    "type": "text",
                    "text": "Title",
                    "position": {"x": 10, "y": 20},
                    "font_size": 32,
                    "color": "#000000",
                },
                {
                    "type": "image",
                    "image_url": "https://example.com/logo.png",
                    "position": {"x": 100, "y": 100},
                    "size": {"width": 200, "height": 100},
                },
            ],
        }

        with patch(
            "dolze_templates.utils.validation.validate_component"
        ) as mock_validate_component, patch(
            "dolze_templates.utils.validation.validate_url"
        ) as mock_validate_url:

            # Mock validate_component to return the component as-is
            def mock_validate(component, index):
                return component

            mock_validate_component.side_effect = mock_validate
            mock_validate_url.return_value = "https://example.com/logo.png"

            result = validate_template_config(config)

        self.assertEqual(result["name"], "Full Template")
        self.assertEqual(result["size"], {"width": 800, "height": 600})
        self.assertEqual(result["background_color"], (255, 255, 255, 255))
        self.assertFalse(result["use_base_image"])
        self.assertEqual(len(result["components"]), 2)
        self.assertEqual(result["components"][0]["type"], "text")
        self.assertEqual(result["components"][1]["type"], "image")


if __name__ == "__main__":
    unittest.main()
