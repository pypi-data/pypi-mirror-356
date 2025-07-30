"""
Font Manager - Manages and provides access to custom fonts
"""

import os
import logging
from typing import Dict, Optional, List
from PIL import ImageFont

# Set up logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FontManager:
    """
    Manages font loading and provides access to custom fonts.
    """

    def __init__(self, font_dir: str = "fonts"):
        """
        Initialize the font manager.

        Args:
            font_dir: Directory containing font files
        """
        self.font_dir = font_dir
        self.fonts: Dict[str, str] = {}
        self._scan_fonts()

    def _scan_fonts(self) -> None:
        """
        Recursively scan the font directory and its subdirectories for available fonts.
        Fonts are stored with their base filename (without extension) as the key.
        """
        if not os.path.exists(self.font_dir):
            os.makedirs(self.font_dir, exist_ok=True)
            return

        for root, _, files in os.walk(self.font_dir):
            for filename in files:
                if filename.lower().endswith((".ttf", ".otf")):
                    font_name = os.path.splitext(filename)[0]
                    font_path = os.path.join(root, filename)
                    self.fonts[font_name] = font_path
                    logger.debug(f"Found font: {font_name} at {font_path}")

    def get_font_path(self, font_name: str) -> Optional[str]:
        """
        Get the path to a font file by name.

        Args:
            font_name: Name of the font (without extension)

        Returns:
            Path to the font file or None if not found
        """
        return self.fonts.get(font_name)

    def get_font(
        self, font_name: Optional[str] = None, size: int = 24
    ) -> ImageFont.FreeTypeFont:
        """
        Get a font by name and size.

        Args:
            font_name: Name of the font (without extension)
            size: Font size

        Returns:
            PIL ImageFont object
        """
        # If no font name is specified, use the first available font
        if font_name is None and self.fonts:
            font_path = next(iter(self.fonts.values()))
        elif font_name in self.fonts:
            font_path = self.fonts[font_name]
            logger.debug(f"Loading font: {font_name} from {font_path}")
        else:
            # If the requested font is not available, try to use a default system font
            try:
                # Common system fonts
                system_fonts = [
                    "/System/Library/Fonts/Helvetica.ttc",  # macOS
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
                    "C:\\Windows\\Fonts\\arial.ttf",  # Windows
                ]

                for font in system_fonts:
                    if os.path.exists(font):
                        return ImageFont.truetype(font, size)

                # If no system fonts are available, use the default font
                return ImageFont.load_default()
            except Exception as e:
                logger.warning(f"Failed to load system font: {e}")
                return ImageFont.load_default()

        try:
            return ImageFont.truetype(font_path, size)
        except Exception as e:
            logger.error(f"Failed to load font {font_path}: {e}")
            # Fallback to default font if loading fails
            return ImageFont.load_default()

    def list_fonts(self) -> List[str]:
        """
        Get a list of available font names.

        Returns:
            List of font names
        """
        return list(self.fonts.keys())


# Singleton instance for easy access
_instance = None


def get_font_manager(font_dir: str = "fonts") -> FontManager:
    """
    Get the singleton instance of the font manager.

    Args:
        font_dir: Directory containing font files

    Returns:
        FontManager instance
    """
    global _instance
    if _instance is None:
        _instance = FontManager(font_dir)
    return _instance
