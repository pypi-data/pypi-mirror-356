"""
Button components for interactive elements in templates.
"""

from typing import Tuple, Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont
from .base import Component
from dolze_image_templates.core.font_manager import get_font_manager


class CTAButtonComponent(Component):
    """Component for rendering CTA buttons"""

    def __init__(
        self,
        text: str,
        position: Tuple[int, int] = (0, 0),
        size: Tuple[int, int] = (200, 50),
        bg_color: Tuple[int, int, int] = (0, 123, 255),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        corner_radius: int = 10,
        font_size: int = 18,
        font_path: Optional[str] = None,
        url: Optional[str] = None,
    ):
        """
        Initialize a CTA button component.

        Args:
            text: Button text
            position: Position (x, y) of the button
            size: Size (width, height) of the button
            bg_color: RGB color tuple for button background
            text_color: RGB color tuple for button text
            corner_radius: Radius for rounded corners
            font_size: Font size in points
            font_path: Path to a TTF font file or font name
            url: URL to link to (for metadata)
        """
        super().__init__(position)
        self.text = text
        self.size = size
        self.bg_color = bg_color
        self.text_color = text_color
        self.corner_radius = corner_radius
        self.font_size = font_size
        self.font_path = font_path
        self.url = url
        self._font = None

    def _get_font(self) -> ImageFont.FreeTypeFont:
        """Get the font for the button text"""
        if self._font is None:
            font_manager = get_font_manager()
            self._font = font_manager.get_font(self.font_path, self.font_size)
        return self._font

    def _draw_rounded_rect(
        self,
        draw: ImageDraw.Draw,
        bbox: Tuple[int, int, int, int],
        radius: int,
        **kwargs,
    ):
        """Draw a rounded rectangle"""
        x1, y1, x2, y2 = bbox

        # Draw four rounded corners
        draw.ellipse((x1, y1, x1 + 2 * radius, y1 + 2 * radius), **kwargs)  # Top-left
        draw.ellipse((x2 - 2 * radius, y1, x2, y1 + 2 * radius), **kwargs)  # Top-right
        draw.ellipse(
            (x1, y2 - 2 * radius, x1 + 2 * radius, y2), **kwargs
        )  # Bottom-left
        draw.ellipse(
            (x2 - 2 * radius, y2 - 2 * radius, x2, y2), **kwargs
        )  # Bottom-right

        # Draw rectangles for the sides and center
        draw.rectangle((x1 + radius, y1, x2 - radius, y2), **kwargs)  # Horizontal
        draw.rectangle((x1, y1 + radius, x2, y2 - radius), **kwargs)  # Vertical

    def render(self, image: Image.Image) -> Image.Image:
        """Render a CTA button onto an image"""
        result = image.copy()
        draw = ImageDraw.Draw(result, "RGBA")

        # Calculate button position and size
        x, y = self.position
        width, height = self.size
        bbox = [x, y, x + width, y + height]

        # Draw the button background with rounded corners
        self._draw_rounded_rect(
            draw,
            bbox,
            self.corner_radius,
            fill=self.bg_color + (255,),  # Add alpha channel
        )

        # Draw the button text
        font = self._get_font()
        text_width = draw.textlength(self.text, font=font)
        text_x = x + (width - text_width) // 2
        text_y = y + (height - self.font_size) // 2 - 2  # Small vertical adjustment

        draw.text(
            (text_x, text_y),
            self.text,
            font=font,
            fill=self.text_color,
        )

        return result

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "CTAButtonComponent":
        """Create a CTA button component from a configuration dictionary"""
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0),
        )

        size = (
            config.get("size", {}).get("width", 200),
            config.get("size", {}).get("height", 50),
        )

        # Handle colors which might be lists or tuples
        bg_color = config.get("bg_color", (0, 123, 255))
        if isinstance(bg_color, (list, tuple)) and len(bg_color) >= 3:
            bg_color = tuple(bg_color[:3])

        text_color = config.get("text_color", (255, 255, 255))
        if isinstance(text_color, (list, tuple)) and len(text_color) >= 3:
            text_color = tuple(text_color[:3])

        return cls(
            text=config.get("text", "Click Here"),
            position=position,
            size=size,
            bg_color=bg_color,
            text_color=text_color,
            corner_radius=config.get("corner_radius", 10),
            font_size=config.get("font_size", 18),
            font_path=config.get("font_path"),
            url=config.get("url"),
        )
