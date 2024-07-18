import numpy as np
from typing import Tuple

class ImageLogic:
    """Core logic for manipulating pixel art images."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.image = np.full((height, width, 4), 255, dtype=np.uint8)  # RGBA image

    def set_pixel(self, x: int, y: int, colour: Tuple[int, int, int, int]):
        """Set the colour of a pixel."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.image[y, x] = colour

    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """Get the colour of a pixel."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return tuple(self.image[y, x])
        return (0, 0, 0, 0)  # Return transparent black if out of bounds

    def fill(self, x: int, y: int, new_colour: Tuple[int, int, int, int]):
        """Fill an area with a new colour."""
        old_colour = self.get_pixel(x, y)
        if old_colour == new_colour:
            return

        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if self.get_pixel(cx, cy) == old_colour:
                self.set_pixel(cx, cy, new_colour)
                if cx > 0:
                    stack.append((cx - 1, cy))
                if cx < self.width - 1:
                    stack.append((cx + 1, cy))
                if cy > 0:
                    stack.append((cx, cy - 1))
                if cy < self.height - 1:
                    stack.append((cx, cy + 1))

    def clear(self, colour: Tuple[int, int, int, int] = (255, 255, 255, 255)):
        """Clear the entire image with a specified colour."""
        self.image.fill(colour)

    def resize(self, new_width: int, new_height: int):
        """Resize the image."""
        new_image = np.full((new_height, new_width, 4), 255, dtype=np.uint8)
        new_image[:min(new_height, self.height), :min(new_width, self.width)] = self.image[:min(new_height, self.height), :min(new_width, self.width)]
        self.image = new_image
        self.width = new_width
        self.height = new_height