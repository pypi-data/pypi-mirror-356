"""
Unit tests for the Dolze Templates components.
"""

import os
import unittest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add parent directory to path so we can import the package
import sys

sys.path.append(str(Path(__file__).parent.parent))

from dolze_templates.components import (
    Component,
    TextComponent,
    ImageComponent,
    CircleComponent,
    RectangleComponent,
    CTAButtonComponent,
    FooterComponent,
    create_component_from_config,
)
from dolze_templates.utils.validation import (
    validate_color,
    validate_position,
    validate_size,
)


class TestBaseComponent(unittest.TestCase):
    "Test case for the base Component class."

    def test_component_initialization(self):
        "Test that a component can be initialized with default values."
        component = Component("test")
        self.assertEqual(component.name, "test")
        self.assertEqual(component.position, (0, 0))
        self.assertIsNone(component.size)
        self.assertTrue(component.visible)

    def test_component_to_dict(self):
        "Test converting a component to a dictionary."
        component = Component("test", position=(10, 20), size=(100, 200), visible=False)
        component_dict = component.to_dict()

        self.assertEqual(component_dict["type"], "component")
        self.assertEqual(component_dict["position"], {"x": 10, "y": 20})
        self.assertEqual(component_dict["size"], {"width": 100, "height": 200})
        self.assertFalse(component_dict["visible"])


class TestTextComponent(unittest.TestCase):
    "Test case for the TextComponent class."

    def setUp(self):
        "Set up test fixtures."
        self.text = "Test Text"
        self.position = (50, 50)
        self.font_size = 24
        self.color = (0, 0, 0, 255)
        self.component = TextComponent(
            text=self.text,
            position=self.position,
            font_size=self.font_size,
            color=self.color,
        )

    def test_text_component_initialization(self):
        "Test that a text component can be initialized."
        self.assertEqual(self.component.text, self.text)
        self.assertEqual(self.component.position, self.position)
        self.assertEqual(self.component.font_size, self.font_size)
        self.assertEqual(self.component.color, self.color)
        self.assertEqual(self.component.alignment, "left")

    def test_text_component_to_dict(self):
        "Test converting a text component to a dictionary."
        component_dict = self.component.to_dict()

        self.assertEqual(component_dict["type"], "text")
        self.assertEqual(component_dict["text"], self.text)
        self.assertEqual(
            component_dict["position"], {"x": self.position[0], "y": self.position[1]}
        )
        self.assertEqual(component_dict["font_size"], self.font_size)
        self.assertEqual(component_dict["color"], list(self.color))

    @patch("PIL.ImageDraw.Draw.text")
    @patch("PIL.ImageDraw.Draw.multiline_textbbox")
    def test_render(self, mock_textbbox, mock_draw):
        "Test rendering a text component."
        # Mock the text bbox to return a fixed size
        mock_textbbox.return_value = (0, 0, 100, 50)

        # Create a mock image
        mock_image = MagicMock()
        mock_draw.return_value = MagicMock()

        # Render the component
        self.component.render(mock_image, {})

        # Check that the text was drawn
        mock_draw.return_value.text.assert_called_once()


class TestImageComponent(unittest.TestCase):
    "Test case for the ImageComponent class."

    def setUp(self):
        "Set up test fixtures."
        self.image_path = "test_image.jpg"
        self.position = (100, 100)
        self.size = (200, 200)
        self.component = ImageComponent(
            image_path=self.image_path, position=self.position, size=self.size
        )

    def test_image_component_initialization(self):
        "Test that an image component can be initialized."
        self.assertEqual(self.component.image_path, self.image_path)
        self.assertEqual(self.component.position, self.position)
        self.assertEqual(self.component.size, self.size)
        self.assertFalse(self.component.circle_crop)

    @patch("PIL.Image.open")
    def test_load_image_from_path(self, mock_open):
        "Test loading an image from a file path."
        # Mock the image open and size
        mock_img = MagicMock()
        mock_img.size = (400, 400)
        mock_open.return_value = mock_img

        # Test loading the image
        img = self.component._load_image()

        # Check that the image was opened and resized
        mock_open.assert_called_once_with(self.image_path)
        mock_img.resize.assert_called_once()
        self.assertIsNotNone(img)

    @patch("requests.get")
    def test_load_image_from_url(self, mock_get):
        "Test loading an image from a URL."
        # Create a component with a URL
        component = ImageComponent(
            image_url="http://example.com/image.jpg",
            position=self.position,
            size=self.size,
        )

        # Mock the response
        mock_response = MagicMock()
        mock_response.content = b"fake image data"
        mock_get.return_value = mock_response

        # Mock the Image.open to return a mock image
        with patch("PIL.Image.open") as mock_open:
            mock_img = MagicMock()
            mock_img.size = (400, 400)
            mock_open.return_value = mock_img

            # Test loading the image
            img = component._load_image()

            # Check that the image was loaded from the URL
            mock_get.assert_called_once_with(
                "http://example.com/image.jpg", stream=True
            )
            self.assertIsNotNone(img)


class TestComponentFactory(unittest.TestCase):
    "Test case for the component factory function."

    def test_create_text_component(self):
        "Test creating a text component from a config dictionary."
        config = {
            "type": "text",
            "text": "Hello, World!",
            "position": {"x": 10, "y": 20},
            "font_size": 24,
            "color": [0, 0, 0, 255],
        }

        component = create_component_from_config(config)

        self.assertIsInstance(component, TextComponent)
        self.assertEqual(component.text, "Hello, World!")
        self.assertEqual(component.position, (10, 20))
        self.assertEqual(component.font_size, 24)

    def test_create_image_component(self):
        "Test creating an image component from a config dictionary."
        config = {
            "type": "image",
            "image_path": "test.jpg",
            "position": {"x": 0, "y": 0},
            "size": {"width": 100, "height": 100},
        }

        component = create_component_from_config(config)

        self.assertIsInstance(component, ImageComponent)
        self.assertEqual(component.image_path, "test.jpg")
        self.assertEqual(component.size, (100, 100))

    def test_create_circle_component(self):
        "Test creating a circle component from a config dictionary."
        config = {
            "type": "circle",
            "position": {"x": 100, "y": 100},
            "radius": 50,
            "fill_color": [255, 0, 0, 255],
        }

        component = create_component_from_config(config)

        self.assertIsInstance(component, CircleComponent)
        self.assertEqual(component.position, (100, 100))
        self.assertEqual(component.radius, 50)
        self.assertEqual(component.fill_color, (255, 0, 0, 255))

    def test_create_rectangle_component(self):
        "Test creating a rectangle component from a config dictionary."
        config = {
            "type": "rectangle",
            "position": {"x": 10, "y": 10},
            "size": {"width": 100, "height": 50},
            "fill_color": [0, 0, 255, 255],
            "outline_color": [0, 0, 0, 255],
            "outline_width": 2,
        }

        component = create_component_from_config(config)

        self.assertIsInstance(component, RectangleComponent)
        self.assertEqual(component.position, (10, 10))
        self.assertEqual(component.size, (100, 50))
        self.assertEqual(component.fill_color, (0, 0, 255, 255))
        self.assertEqual(component.outline_color, (0, 0, 0, 255))
        self.assertEqual(component.outline_width, 2)

    def test_create_cta_button_component(self):
        "Test creating a CTA button component from a config dictionary."
        config = {
            "type": "cta_button",
            "text": "Click Me",
            "position": {"x": 10, "y": 10},
            "size": {"width": 200, "height": 50},
            "bg_color": [0, 123, 255, 255],
            "text_color": [255, 255, 255, 255],
            "corner_radius": 5,
        }

        component = create_component_from_config(config)

        self.assertIsInstance(component, CTAButtonComponent)
        self.assertEqual(component.text, "Click Me")
        self.assertEqual(component.position, (10, 10))
        self.assertEqual(component.size, (200, 50))
        self.assertEqual(component.bg_color, (0, 123, 255, 255))
        self.assertEqual(component.text_color, (255, 255, 255, 255))
        self.assertEqual(component.corner_radius, 5)

    def test_create_footer_component(self):
        "Test creating a footer component from a config dictionary."
        config = {
            "type": "footer",
            "text": "© 2023 My Company",
            "position": {"x": 0, "y": 580},
            "font_size": 14,
            "color": [255, 255, 255, 200],
            "bg_color": [0, 0, 0, 100],
            "padding": 10,
        }

        component = create_component_from_config(config)

        self.assertIsInstance(component, FooterComponent)
        self.assertEqual(component.text, "© 2023 My Company")
        self.assertEqual(component.position, (0, 580))
        self.assertEqual(component.font_size, 14)
        self.assertEqual(component.color, (255, 255, 255, 200))
        self.assertEqual(component.bg_color, (0, 0, 0, 100))
        self.assertEqual(component.padding, 10)


class TestValidationUtils(unittest.TestCase):
    "Test case for validation utility functions."

    def test_validate_color(self):
        "Test color validation."
        # Test hex color
        self.assertEqual(validate_color("#FF0000"), (255, 0, 0, 255))
        self.assertEqual(validate_color("#00FF00FF"), (0, 255, 0, 255))

        # Test RGB tuple
        self.assertEqual(validate_color((255, 0, 0)), (255, 0, 0, 255))

        # Test RGBA tuple
        self.assertEqual(validate_color((0, 255, 0, 128)), (0, 255, 0, 128))

        # Test invalid colors
        with self.assertRaises(ValueError):
            validate_color("not a color")

        with self.assertRaises(ValueError):
            validate_color((300, 0, 0))  # Invalid RGB value

    def test_validate_position(self):
        "Test position validation."
        # Test dict position
        self.assertEqual(validate_position({"x": 10, "y": 20}), (10, 20))

        # Test tuple position
        self.assertEqual(validate_position((30, 40)), (30, 40))

        # Test invalid positions
        with self.assertRaises(ValueError):
            validate_position("not a position")

        with self.assertRaises(ValueError):
            validate_position((1, 2, 3))  # Too many values

    def test_validate_size(self):
        "Test size validation."
        # Test dict size
        self.assertEqual(validate_size({"width": 100, "height": 200}), (100, 200))

        # Test tuple size
        self.assertEqual(validate_size((300, 400)), (300, 400))

        # Test invalid sizes
        with self.assertRaises(ValueError):
            validate_size({"width": -10, "height": 100})  # Negative width

        with self.assertRaises(ValueError):
            validate_size((1, 2, 3))  # Too many values


if __name__ == "__main__":
    unittest.main()
