import os
import sys
import customtkinter as ctk
import pygame
from src.components.palette import Palette
from src.components.canvas import Canvas
from src.components.toolbox import Toolbox
from src.core.image_logic import ImageLogic
from src.logging import get_logger

logger = get_logger(__name__)

class PixelScribeApp(ctk.CTk):
    """Main application class for Pixel Scribe."""

    def __init__(self):
        super().__init__()

        self.title("Pixel Scribe")
        self.geometry("800x600")

        # Initialize Pygame
        pygame.init()

        # Create a left panel for toolbox and palette
        self.left_panel = ctk.CTkFrame(self)
        self.left_panel.pack(side="left", fill="y", padx=5, pady=5)

        # Initialize components
        self.toolbox = Toolbox(self.left_panel)
        self.palette = Palette(self.left_panel)
        self.canvas = Canvas(self)
        self.image_logic = ImageLogic(64, 64)  # Default 64x64 pixel grid

        # Layout components
        self.toolbox.pack(side="top", fill="x", pady=(0, 10))
        self.palette.pack(side="top", fill="x")
        self.canvas.pack(side="right", expand=True, fill="both", padx=5, pady=5)

        # Bind events
        self.bind("<MouseWheel>", self.adjust_brush_size)

        logger.info("PixelScribe application initialized")

    def adjust_brush_size(self, event):
        """Adjust brush size using the mouse wheel."""
        if self.toolbox.get_current_tool() in ["brush", "eraser"]:
            delta = event.delta // 120  # Normalize delta
            new_size = max(1, min(10, self.toolbox.brush_size + delta))
            self.toolbox.set_brush_size(new_size)
            self.canvas.set_brush_size(new_size)
            logger.debug(f"Brush size adjusted to {new_size}")

def main():
    ctk.set_appearance_mode("dark")  # Set the appearance mode to dark
    ctk.set_default_color_theme("blue")  # Set the color theme to blue
    app = PixelScribeApp()
    logger.info("Starting PixelScribe application")
    app.mainloop()

if __name__ == "__main__":
    main()