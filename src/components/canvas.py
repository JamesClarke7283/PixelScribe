import customtkinter as ctk
import pygame
from PIL import Image, ImageDraw, ImageTk
import numpy as np
from src.logging import get_logger

logger = get_logger(__name__)

class Canvas(ctk.CTkFrame):
    """Canvas component for pixel art drawing."""

    def __init__(self, master):
        super().__init__(master)
        self.width = 512  # Default canvas size
        self.height = 512
        self.pixel_size = 8  # 64x64 grid
        self.brush_size = 1
        self.brush_shape = "square"
        self.zoom_level = 1
        self.create_widgets()

    def create_widgets(self):
        """Create and layout the canvas widgets."""
        self.pygame_surface = pygame.Surface((self.width, self.height))
        self.pygame_surface.fill((255, 255, 255))  # White background

        self.canvas = ctk.CTkCanvas(
            self,
            width=self.width,
            height=self.height,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(expand=True)

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<B3-Motion>", self.on_right_drag)
        self.canvas.bind("<Motion>", self.on_hover)

        self.photo_image = None
        self.image_on_canvas = None
        self.hover_overlay = None
        self.update_canvas()

    def update_canvas(self):
        """Update the CustomTkinter canvas with the Pygame surface."""
        pygame_image = pygame.image.tostring(self.pygame_surface, "RGB", False)
        image = Image.frombytes("RGB", (self.width, self.height), pygame_image)
        image = image.resize((int(self.width * self.zoom_level), int(self.height * self.zoom_level)))
        photo = ImageTk.PhotoImage(image)
        
        if self.image_on_canvas:
            self.canvas.delete(self.image_on_canvas)
        
        self.photo_image = photo  # Keep a reference to avoid garbage collection
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

    def draw_pixel(self, x: int, y: int, colour: str):
        """Draw pixels on the canvas based on brush size and shape."""
        color = pygame.Color(colour)
        brush_pixels = self.get_brush_pixels(x, y)
        for px, py in brush_pixels:
            pygame.draw.rect(
                self.pygame_surface,
                color,
                (px * self.pixel_size, py * self.pixel_size, self.pixel_size, self.pixel_size)
            )
        self.update_canvas()

    def get_brush_pixels(self, x: int, y: int):
        """Get the pixels covered by the brush based on its size and shape."""
        center_x, center_y = int(x / self.zoom_level) // self.pixel_size, int(y / self.zoom_level) // self.pixel_size
        pixels = []
        
        if self.brush_shape == "square":
            for dx in range(-self.brush_size // 2 + 1, self.brush_size // 2 + 1):
                for dy in range(-self.brush_size // 2 + 1, self.brush_size // 2 + 1):
                    px, py = center_x + dx, center_y + dy
                    if 0 <= px < self.width // self.pixel_size and 0 <= py < self.height // self.pixel_size:
                        pixels.append((px, py))
        
        return pixels

    def on_left_click(self, event):
        """Handle left mouse button press event."""
        tool = self.master.toolbox.get_current_tool()
        if tool == "brush":
            self.draw_pixel(event.x, event.y, self.master.palette.get_current_color())
        elif tool == "eraser":
            self.draw_pixel(event.x, event.y, "#FFFFFF")
        elif tool == "dropper":
            color = self.get_pixel_color(event.x, event.y)
            self.master.palette.set_color(color)
        elif tool == "fill":
            self.fill(event.x, event.y, self.master.palette.get_current_color())
        elif tool == "zoom":
            self.zoom(1.2)

    def on_left_drag(self, event):
        """Handle left mouse drag event."""
        tool = self.master.toolbox.get_current_tool()
        if tool in ["brush", "eraser"]:
            color = self.master.palette.get_current_color() if tool == "brush" else "#FFFFFF"
            self.draw_pixel(event.x, event.y, color)

    def on_right_click(self, event):
        """Handle right mouse button press event."""
        tool = self.master.toolbox.get_current_tool()
        if tool == "zoom":
            self.zoom(0.8)

    def on_right_drag(self, event):
        """Handle right mouse drag event."""
        pass  # Implement if needed

    def on_hover(self, event):
        """Handle mouse hover event to show brush preview."""
        if self.hover_overlay:
            self.canvas.delete(self.hover_overlay)

        brush_pixels = self.get_brush_pixels(event.x, event.y)
        overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        for px, py in brush_pixels:
            draw.rectangle(
                [px * self.pixel_size * self.zoom_level, py * self.pixel_size * self.zoom_level, 
                 (px + 1) * self.pixel_size * self.zoom_level, (py + 1) * self.pixel_size * self.zoom_level],
                fill=(128, 128, 128, 128)
            )

        overlay_photo = ImageTk.PhotoImage(overlay)
        self.hover_overlay = self.canvas.create_image(0, 0, anchor="nw", image=overlay_photo)
        self.canvas.overlay_photo = overlay_photo  # Keep a reference

    def get_pixel_color(self, x: int, y: int) -> str:
        """Get the color of a pixel at the given coordinates."""
        px, py = int(x / self.zoom_level) // self.pixel_size, int(y / self.zoom_level) // self.pixel_size
        color = self.pygame_surface.get_at((px * self.pixel_size, py * self.pixel_size))
        return f"#{color.r:02x}{color.g:02x}{color.b:02x}"

    def fill(self, x: int, y: int, new_color: str):
        """Fill an area with a new color."""
        px, py = int(x / self.zoom_level) // self.pixel_size, int(y / self.zoom_level) // self.pixel_size
        old_color = self.get_pixel_color(x, y)
        if old_color == new_color:
            return

        stack = [(px, py)]
        while stack:
            cx, cy = stack.pop()
            if self.get_pixel_color(cx * self.pixel_size, cy * self.pixel_size) == old_color:
                self.draw_pixel(cx * self.pixel_size, cy * self.pixel_size, new_color)
                if cx > 0:
                    stack.append((cx - 1, cy))
                if cx < self.width // self.pixel_size - 1:
                    stack.append((cx + 1, cy))
                if cy > 0:
                    stack.append((cx, cy - 1))
                if cy < self.height // self.pixel_size - 1:
                    stack.append((cx, cy + 1))

    def zoom(self, factor: float):
        """Zoom the canvas in or out."""
        self.zoom_level *= factor
        self.zoom_level = max(1, min(10, self.zoom_level))  # Limit zoom between 1x and 10x
        self.update_canvas()

    def set_brush_size(self, size: int):
        """Set the brush size."""
        self.brush_size = size