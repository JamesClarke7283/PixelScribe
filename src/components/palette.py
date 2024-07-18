import customtkinter as ctk
from tkinter import colorchooser
from src.logging import get_logger
from collections import deque

logger = get_logger(__name__)

class Palette(ctk.CTkFrame):
    """Palette component for colour selection."""

    def __init__(self, master):
        super().__init__(master)
        self.current_color = "#000000"
        self.colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        self.create_widgets()

    def create_widgets(self):
        """Create and layout the palette widgets."""
        self.color_buttons = []
        for i, color in enumerate(self.colors):
            button = ctk.CTkButton(
                self,
                width=40,
                height=40,
                fg_color=color,
                text="",
                command=lambda c=color: self.set_color(c)
            )
            button.grid(row=i // 2, column=i % 2, padx=2, pady=2)
            button.bind("<Button-3>", lambda event, idx=i: self.open_color_picker(event, idx))
            self.color_buttons.append(button)

    def set_color(self, color):
        """Set the current color."""
        self.current_color = color
        logger.info(f"Changed color to {self.current_color}")

    def open_color_picker(self, event, index):
        """Open color picker and set the selected color."""
        color = colorchooser.askcolor(initialcolor=self.colors[index])[1]
        if color:
            self.colors[index] = color
            self.color_buttons[index].configure(fg_color=color)
            logger.info(f"Changed color at index {index} to {color}")

    def get_current_color(self) -> str:
        """Get the current selected color."""
        return self.current_color