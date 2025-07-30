"""
Dolze Templates - A flexible template generation library for creating social media posts, banners, and more.

This package provides a powerful and extensible system for generating images with text, shapes, and other
components in a template-based approach.
"""

# Version information
__version__ = "0.1.2"

# Core functionality
from .core import (
    Template,
    TemplateEngine,
    TemplateRegistry,
    get_template_registry,
    FontManager,
    get_font_manager,
)
from typing import Optional, Dict, Any


def get_all_image_templates() -> list[str]:
    """
    Get a list of all available template names.

    Returns:
        List[str]: A list of all available template names
    """
    return get_template_registry().get_all_templates()


def render_template(
    template_name: str,
    variables: Optional[Dict[str, Any]] = None,
    output_dir: str = "output",
    output_path: Optional[str] = None,
    output_format: str = "png",
) -> str:
    """
    Render a template with the given variables.

    This is a convenience function that creates a TemplateEngine instance and
    renders a template in one step. The template must be present in the templates directory.

    Args:
        template_name: Name of the template to render (must be in the templates directory)
        variables: Dictionary of variables to substitute in the template
        output_dir: Directory to save the rendered image (used if output_path is None)
        output_path: Full path to save the rendered image. If None, a path will be generated.
        output_format: Output image format (e.g., 'png', 'jpg', 'jpeg')

    Returns:
        Path to the rendered image

    Example:
        ```python
        from dolze_templates import render_template

        # Define template variables
        variables = {
            "title": "Welcome to Dolze",
            "subtitle": "Create amazing images with ease",
            "image_url": "https://example.com/hero.jpg"
        }

        # Render a template from the templates directory
        output_path = render_template(
            template_name="my_template",
            variables=variables,
            output_dir="output"
        )
        print(f"Rendered image saved to: {output_path}")
        ```
    """
    engine = TemplateEngine(output_dir=output_dir)
    return engine.render_template(
        template_name=template_name,
        variables=variables or {},
        output_path=output_path,
        output_format=output_format,
    )


# Resource management and caching
from .resources import load_image, load_font
from .utils.cache import clear_cache, get_cache_info

# Components
from .components import (
    Component,
    TextComponent,
    ImageComponent,
    CircleComponent,
    RectangleComponent,
    CTAButtonComponent,
    FooterComponent,
    create_component_from_config,
)

# Configuration
from .config import (
    Settings,
    get_settings,
    configure,
    DEFAULT_TEMPLATES_DIR,
    DEFAULT_FONTS_DIR,
    DEFAULT_OUTPUT_DIR,
)

# Version
__version__ = "0.1.2"


# Package metadata
__author__ = "Dolze Team"
__email__ = "support@dolze.com"
__license__ = "MIT"
__description__ = "A flexible template generation library for creating social media posts, banners, and more."


# Package-level initialization
def init() -> None:
    """
    Initialize the Dolze Templates package.
    This function ensures all required directories exist and performs any necessary setup.
    """
    settings = get_settings()

    # Ensure required directories exist
    import os

    os.makedirs(settings.templates_dir, exist_ok=True)
    os.makedirs(settings.fonts_dir, exist_ok=True)
    os.makedirs(settings.output_dir, exist_ok=True)


# Initialize the package when imported
init()


# Clean up namespace
del init

__all__ = [
    # Core
    "Template",
    "TemplateEngine",
    "TemplateRegistry",
    "get_template_registry",
    "FontManager",
    "get_font_manager",
    # Components
    "Component",
    "TextComponent",
    "ImageComponent",
    "CircleComponent",
    "RectangleComponent",
    "CTAButtonComponent",
    "FooterComponent",
    "create_component_from_config",
    # Configuration
    "Settings",
    "get_settings",
    "configure",
    "DEFAULT_TEMPLATES_DIR",
    "DEFAULT_FONTS_DIR",
    "DEFAULT_OUTPUT_DIR",
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__description__",
]
