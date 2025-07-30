"""
Shape components for rendering basic shapes in templates.
"""

from typing import Tuple, Optional, Dict, Any, List
from PIL import Image, ImageDraw
from .base import Component


class CircleComponent(Component):
    """Component for rendering circles with optional background images"""

    def __init__(
        self,
        position: Tuple[int, int] = (0, 0),
        radius: int = 50,
        fill_color: Optional[Tuple[int, int, int]] = (200, 200, 200),
        outline_color: Optional[Tuple[int, int, int]] = None,
        outline_width: int = 2,
        image_url: Optional[str] = None,
        image_path: Optional[str] = None,
    ):
        """
        Initialize a circle component.

        Args:
            position: Position (x, y) of the center of the circle
            radius: Radius of the circle in pixels
            fill_color: RGB color tuple for the circle fill (None for transparent)
            outline_color: RGB color tuple for the circle outline (None for no outline)
            outline_width: Width of the outline in pixels
            image_url: URL of an image to display inside the circle
            image_path: Path to a local image file to display inside the circle
        """
        super().__init__(position)
        self.radius = radius
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.image_url = image_url
        self.image_path = image_path
        self._cached_image = None

    def _load_image(self) -> Optional[Image.Image]:
        """Load image from URL or path if not already loaded"""
        if self._cached_image is not None:
            return self._cached_image

        # Try to load from URL first, then from path
        if self.image_url:
            try:
                response = requests.get(self.image_url)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                self._cached_image = img.convert("RGBA")
                return self._cached_image
            except (requests.RequestException, IOError):
                pass

        if self.image_path and os.path.exists(self.image_path):
            try:
                img = Image.open(self.image_path)
                self._cached_image = img.convert("RGBA")
                return self._cached_image
            except IOError:
                pass

        return None

    def render(self, image: Image.Image) -> Image.Image:
        """Render the circle onto an image"""
        result = image.copy()
        draw = ImageDraw.Draw(result)

        # Calculate bounding box
        x, y = self.position
        bbox = [
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius,
        ]

        # Draw the circle
        if self.fill_color is not None:
            draw.ellipse(bbox, fill=self.fill_color)

        if self.outline_color is not None and self.outline_width > 0:
            draw.ellipse(bbox, outline=self.outline_color, width=self.outline_width)

        # If there's an image, draw it inside the circle
        img = self._load_image()
        if img is not None:
            # Resize image to fit the circle
            size = (self.radius * 2, self.radius * 2)
            img = img.resize(size, Image.Resampling.LANCZOS)

            # Create circular mask
            mask = Image.new("L", size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, size[0], size[1]), fill=255)

            # Apply mask and paste
            result.paste(img, (x - self.radius, y - self.radius), mask)

        return result

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "CircleComponent":
        """Create a circle component from a configuration dictionary"""
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0),
        )

        # Handle color which might be a list or tuple
        fill_color = config.get("fill_color")
        if (
            fill_color
            and isinstance(fill_color, (list, tuple))
            and len(fill_color) >= 3
        ):
            fill_color = tuple(fill_color[:3])

        outline_color = config.get("outline_color")
        if (
            outline_color
            and isinstance(outline_color, (list, tuple))
            and len(outline_color) >= 3
        ):
            outline_color = tuple(outline_color[:3])

        return cls(
            position=position,
            radius=config.get("radius", 50),
            fill_color=fill_color,
            outline_color=outline_color,
            outline_width=config.get("outline_width", 2),
            image_url=config.get("image_url"),
            image_path=config.get("image_path"),
        )


class RectangleComponent(Component):
    """Component for rendering rectangles"""

    def __init__(
        self,
        position: Tuple[int, int] = (0, 0),
        size: Tuple[int, int] = (100, 50),
        fill_color: Optional[Tuple[int, int, int]] = None,
        outline_color: Optional[Tuple[int, int, int]] = None,
        outline_width: int = 1,
        border_radius: int = 0,
    ):
        """
        Initialize a rectangle component.

        Args:
            position: Position (x, y) of the top-left corner
            size: Size (width, height) of the rectangle
            fill_color: RGB color tuple for the fill color (None for transparent)
            outline_color: RGB color tuple for the outline (None for no outline)
            outline_width: Width of the outline in pixels
            border_radius: Radius of the corners in pixels (0 for square corners)
        """
        super().__init__(position)
        self.size = size
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.border_radius = border_radius

    def render(self, image: Image.Image) -> Image.Image:
        """
        Render a rectangle onto an image.

        Args:
            image: The image to render the rectangle on

        Returns:
            The image with the rectangle rendered on it
        """
        result = image.copy()
        draw = ImageDraw.Draw(result)

        # Calculate bounding box
        x, y = self.position
        width, height = self.size
        bbox = [x, y, x + width, y + height]

        # Draw the rectangle with optional rounded corners
        if self.border_radius > 0:
            # Draw filled rectangle with rounded corners
            if self.fill_color is not None:
                draw.rounded_rectangle(
                    bbox, radius=self.border_radius, fill=self.fill_color, outline=None
                )

            # Draw outline with rounded corners if specified
            if self.outline_color is not None and self.outline_width > 0:
                # For outline, we need to draw a slightly smaller rectangle to prevent antialiasing issues
                half_width = self.outline_width / 2
                outline_bbox = [
                    bbox[0] + half_width,
                    bbox[1] + half_width,
                    bbox[2] - half_width - 1,  # -1 to account for 0-based indexing
                    bbox[3] - half_width - 1,
                ]
                draw.rounded_rectangle(
                    outline_bbox,
                    radius=max(0, self.border_radius - self.outline_width // 2),
                    outline=self.outline_color,
                    width=self.outline_width,
                )
        else:
            # Original rectangle drawing for backward compatibility
            if self.fill_color is not None:
                draw.rectangle(bbox, fill=self.fill_color)

            if self.outline_color is not None and self.outline_width > 0:
                draw.rectangle(
                    bbox, outline=self.outline_color, width=self.outline_width
                )

        return result

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "RectangleComponent":
        """
        Create a rectangle component from a configuration dictionary.

        Args:
            config: Configuration dictionary

        Returns:
            A new RectangleComponent instance
        """
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0),
        )

        size = (
            config.get("size", {}).get("width", 100),
            config.get("size", {}).get("height", 50),
        )

        # Handle color which might be a list or tuple
        fill_color = config.get("fill_color")
        if (
            fill_color
            and isinstance(fill_color, (list, tuple))
            and len(fill_color) >= 3
        ):
            fill_color = tuple(fill_color[:3])

        outline_color = config.get("outline_color")
        if (
            outline_color
            and isinstance(outline_color, (list, tuple))
            and len(outline_color) >= 3
        ):
            outline_color = tuple(outline_color[:3])

        return cls(
            position=position,
            size=size,
            fill_color=fill_color,
            outline_color=outline_color,
            outline_width=config.get("outline_width", 1),
            border_radius=config.get("border_radius", 0),
        )


class PolygonComponent(Component):
    """Component for rendering polygons (triangles, etc.)"""

    def __init__(
        self,
        position: Tuple[int, int] = (0, 0),
        points: Optional[List[Tuple[int, int]]] = None,
        fill_color: Optional[Tuple[int, int, int]] = None,
        outline_color: Optional[Tuple[int, int, int]] = None,
        outline_width: int = 1,
    ):
        """
        Initialize a polygon component.

        Args:
            position: Position (x, y) offset for all points
            points: List of (x, y) points relative to position
            fill_color: RGB color tuple for the fill color (None for transparent)
            outline_color: RGB color tuple for the outline (None for no outline)
            outline_width: Width of the outline in pixels
        """
        super().__init__(position)
        self.points = points or []
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.outline_width = outline_width

    def render(self, image: Image.Image) -> Image.Image:
        """
        Render a polygon onto an image.

        Args:
            image: The image to render the polygon on

        Returns:
            The image with the polygon rendered on it
        """
        if not self.points:
            return image

        result = image.copy()
        draw = ImageDraw.Draw(result)

        # Convert points to absolute coordinates
        x_offset, y_offset = self.position
        absolute_points = [(x + x_offset, y + y_offset) for x, y in self.points]

        # Draw the polygon
        if self.fill_color is not None:
            draw.polygon(absolute_points, fill=self.fill_color)

        if self.outline_color is not None and self.outline_width > 0:
            draw.polygon(
                absolute_points, outline=self.outline_color, width=self.outline_width
            )

        return result

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "PolygonComponent":
        """
        Create a polygon component from a configuration dictionary.

        Args:
            config: Configuration dictionary

        Returns:
            A new PolygonComponent instance
        """
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0),
        )

        # Get points list from config
        points = config.get("points", [])
        if not isinstance(points, list):
            points = []

        # Handle color which might be a list or tuple
        fill_color = config.get("fill_color")
        if (
            fill_color
            and isinstance(fill_color, (list, tuple))
            and len(fill_color) >= 3
        ):
            fill_color = tuple(fill_color[:3])

        outline_color = config.get("outline_color")
        if (
            outline_color
            and isinstance(outline_color, (list, tuple))
            and len(outline_color) >= 3
        ):
            outline_color = tuple(outline_color[:3])

        return cls(
            position=position,
            points=points,
            fill_color=fill_color,
            outline_color=outline_color,
            outline_width=config.get("outline_width", 1),
        )
