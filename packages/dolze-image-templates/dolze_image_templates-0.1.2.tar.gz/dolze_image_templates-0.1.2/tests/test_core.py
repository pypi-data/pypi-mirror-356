import os
import json
import unittest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

# Add parent directory to path so we can import the package
import sys

sys.path.append(str(Path(__file__).parent.parent))

from dolze_templates.core import (
    Template,
    TemplateEngine,
    TemplateRegistry,
    get_template_registry,
    FontManager,
    get_font_manager,
)
from dolze_templates.components import TextComponent, ImageComponent
from dolze_templates.utils.validation import validate_template_config


class TestTemplate(unittest.TestCase):
    "Test case for the Template class."

    def setUp(self):
        "Set up test fixtures."
        self.components = [
            TextComponent(
                "Test Text", position=(10, 10), font_size=24, color=(0, 0, 0, 255)
            ),
            ImageComponent("test.jpg", position=(100, 100), size=(200, 200)),
        ]

        self.template = Template(
            name="test_template",
            size=(800, 600),
            background_color=(255, 255, 255, 255),
            components=self.components,
            use_base_image=False,
        )

    def test_template_initialization(self):
        "Test that a template can be initialized."
        self.assertEqual(self.template.name, "test_template")
        self.assertEqual(self.template.size, (800, 600))
        self.assertEqual(self.template.background_color, (255, 255, 255, 255))
        self.assertEqual(len(self.template.components), 2)
        self.assertFalse(self.template.use_base_image)

    def test_add_component(self):
        "Test adding a component to the template."
        new_component = TextComponent("New Text", position=(50, 50))
        self.template.add_component(new_component)

        self.assertEqual(len(self.template.components), 3)
        self.assertEqual(self.template.components[-1], new_component)

    def test_remove_component(self):
        "Test removing a component from the template."
        component_to_remove = self.components[0]
        self.template.remove_component(component_to_remove)

        self.assertEqual(len(self.template.components), 1)
        self.assertNotIn(component_to_remove, self.template.components)

    def test_to_dict(self):
        "Test converting a template to a dictionary."
        template_dict = self.template.to_dict()

        self.assertEqual(template_dict["name"], "test_template")
        self.assertEqual(template_dict["size"], {"width": 800, "height": 600})
        self.assertEqual(template_dict["background_color"], [255, 255, 255, 255])
        self.assertEqual(len(template_dict["components"]), 2)
        self.assertFalse(template_dict["use_base_image"])

    @patch("PIL.Image.new")
    @patch("PIL.ImageDraw.Draw")
    def test_render(self, mock_draw, mock_new):
        "Test rendering a template."
        # Mock the image and draw objects
        mock_img = MagicMock()
        mock_new.return_value = mock_img
        mock_draw.return_value = MagicMock()

        # Mock component rendering
        for component in self.template.components:
            component.render = MagicMock()

        # Render the template
        result = self.template.render()

        # Check that the image was created with the correct size and color
        mock_new.assert_called_once_with("RGBA", (800, 600), (255, 255, 255, 255))

        # Check that each component was rendered
        for component in self.template.components:
            component.render.assert_called_once_with(mock_img, {})

        self.assertEqual(result, mock_img)


class TestTemplateEngine(unittest.TestCase):
    "Test case for the TemplateEngine class."

    def setUp(self):
        "Set up test fixtures."
        self.engine = TemplateEngine()
        self.template = Template("test_template", size=(800, 600))

    @patch("PIL.Image.new")
    @patch("PIL.ImageDraw.Draw")
    def test_render_template(self, mock_draw, mock_new):
        "Test rendering a template with the engine."
        # Mock the image and draw objects
        mock_img = MagicMock()
        mock_new.return_value = mock_img
        mock_draw.return_value = MagicMock()

        # Add a text component with a variable
        text_component = TextComponent("Hello, {{name}}!", position=(10, 10))
        self.template.add_component(text_component)

        # Render the template with variable substitution
        context = {"name": "World"}
        result = self.engine.render_template(self.template, context)

        # Check that the text was rendered with the variable substituted
        self.assertEqual(text_component.text, "Hello, World!")
        self.assertEqual(result, mock_img)

    def test_process_component_config(self):
        "Test processing a component configuration with variables."
        config = {
            "type": "text",
            "text": "Hello, {{name}}!",
            "position": {"x": 10, "y": 20},
            "font_size": 24,
            "color": [0, 0, 0, 255],
        }

        context = {"name": "World"}
        processed = self.engine._process_component_config(config, context)

        self.assertEqual(processed["text"], "Hello, World!")
        self.assertEqual(processed["position"]["x"], 10)
        self.assertEqual(processed["position"]["y"], 20)

    def test_process_component_config_nested(self):
        "Test processing a nested component configuration with variables."
        config = {
            "type": "container",
            "children": [
                {"type": "text", "text": "Hello, {{user.name}}!"},
                {"type": "image", "image_path": "{{user.avatar}}"},
            ],
        }

        context = {"user": {"name": "John", "avatar": "avatar.jpg"}}

        processed = self.engine._process_component_config(config, context)

        self.assertEqual(processed["children"][0]["text"], "Hello, John!")
        self.assertEqual(processed["children"][1]["image_path"], "avatar.jpg")


class TestTemplateRegistry(unittest.TestCase):
    "Test case for the TemplateRegistry class."

    def setUp(self):
        "Set up test fixtures."
        self.temp_dir = tempfile.mkdtemp()
        self.registry = TemplateRegistry(templates_dir=self.temp_dir)

        # Create a test template file
        self.template_data = {
            "name": "test_template",
            "size": {"width": 800, "height": 600},
            "background_color": [255, 255, 255, 255],
            "components": [
                {
                    "type": "text",
                    "text": "Hello, World!",
                    "position": {"x": 10, "y": 10},
                    "font_size": 24,
                    "color": [0, 0, 0, 255],
                }
            ],
        }

        self.template_path = os.path.join(self.temp_dir, "test_template.json")
        with open(self.template_path, "w") as f:
            json.dump(self.template_data, f)

    def tearDown(self):
        "Clean up test fixtures."
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_register_template(self):
        "Test registering a template."
        template = Template.from_dict(self.template_data)
        self.registry.register_template("test_register", template)

        self.assertIn("test_register", self.registry.templates)
        self.assertEqual(self.registry.templates["test_register"], template)

    def test_get_template(self):
        "Test getting a template by name."
        template = Template.from_dict(self.template_data)
        self.registry.register_template("test_get", template)

        result = self.registry.get_template("test_get")
        self.assertEqual(result, template)

        # Test getting a non-existent template
        with self.assertRaises(ValueError):
            self.registry.get_template("non_existent")

    @patch("os.path.exists")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            {
                "name": "test_load",
                "size": {"width": 800, "height": 600},
                "components": [],
            }
        ),
    )
    def test_load_template(self, mock_file, mock_exists):
        "Test loading a template from a file."
        mock_exists.return_value = True

        template = self.registry.load_template("test_load")

        self.assertEqual(template.name, "test_load")
        self.assertEqual(template.size, (800, 600))
        mock_file.assert_called_once()

    @patch("os.path.exists")
    def test_load_template_not_found(self, mock_exists):
        "Test loading a non-existent template file."
        mock_exists.return_value = False

        with self.assertRaises(FileNotFoundError):
            self.registry.load_template("non_existent")

    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_template(self, mock_file, mock_dump):
        "Test saving a template to a file."
        template = Template.from_dict(self.template_data)
        self.registry.save_template("test_save", template)

        mock_file.assert_called_once_with(
            os.path.join(self.temp_dir, "test_save.json"), "w", encoding="utf-8"
        )
        mock_dump.assert_called_once()

    def test_render_template(self):
        "Test rendering a template by name."
        template = Template.from_dict(self.template_data)
        self.registry.register_template("test_render", template)

        # Mock the template's render method
        template.render = MagicMock()

        # Render the template
        context = {"name": "World"}
        self.registry.render_template("test_render", context)

        # Check that the template's render method was called with the context
        template.render.assert_called_once_with(context)


class TestFontManager(unittest.TestCase):
    "Test case for the FontManager class."

    def setUp(self):
        "Set up test fixtures."
        self.temp_dir = tempfile.mkdtemp()
        self.font_manager = FontManager(fonts_dir=self.temp_dir)

        # Create a test font file
        self.font_path = os.path.join(self.temp_dir, "test_font.ttf")
        with open(self.font_path, "wb") as f:
            f.write(b"dummy font data")

    def tearDown(self):
        "Clean up test fixtures."
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_add_font(self):
        "Test adding a font to the manager."
        self.font_manager.add_font("TestFont", self.font_path)

        self.assertIn("TestFont", self.font_manager.fonts)
        self.assertEqual(self.font_manager.fonts["TestFont"], self.font_path)

    @patch("PIL.ImageFont.truetype")
    def test_get_font(self, mock_truetype):
        "Test getting a font with a specific size."
        # Mock the ImageFont.truetype function
        mock_font = MagicMock()
        mock_truetype.return_value = mock_font

        # Add a test font
        self.font_manager.add_font("TestFont", self.font_path)

        # Get the font with a specific size
        font = self.font_manager.get_font("TestFont", 24)

        # Check that the font was loaded with the correct path and size
        mock_truetype.assert_called_once_with(self.font_path, 24)
        self.assertEqual(font, mock_font)

    @patch("PIL.ImageFont.truetype")
    def test_get_font_with_fallback(self, mock_truetype):
        "Test getting a font with fallback to default."
        # Mock the ImageFont.truetype function to raise an IOError for the first call
        mock_truetype.side_effect = [IOError("Font not found"), MagicMock()]

        # Add a test font as the default
        self.font_manager.default_font = "TestFont"
        self.font_manager.add_font("TestFont", self.font_path)

        # Try to get a non-existent font, should fall back to default
        font = self.font_manager.get_font("NonExistentFont", 24)

        # Check that the default font was loaded
        self.assertIsNotNone(font)
        mock_truetype.assert_called_with(self.font_path, 24)

    def test_load_fonts_from_directory(self):
        "Test loading fonts from a directory."
        # Create a subdirectory with font files
        os.makedirs(os.path.join(self.temp_dir, "subdir"))
        font1 = os.path.join(self.temp_dir, "font1.ttf")
        font2 = os.path.join(self.temp_dir, "subdir", "font2.ttf")

        with open(font1, "wb") as f:
            f.write(b"font1 data")
        with open(font2, "wb") as f:
            f.write(b"font2 data")

        # Load fonts from the directory
        self.font_manager.load_fonts_from_directory(self.temp_dir)

        # Check that both fonts were loaded with the correct names
        self.assertIn("font1", self.font_manager.fonts)
        self.assertIn("font2", self.font_manager.fonts)
        self.assertEqual(self.font_manager.fonts["font1"], font1)
        self.assertEqual(self.font_manager.fonts["font2"], font2)


if __name__ == "__main__":
    unittest.main()
