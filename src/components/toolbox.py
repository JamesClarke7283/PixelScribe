import customtkinter as ctk
from PIL import Image
from src.utils import get_cached_image, print_debug_info
from src.logging import get_logger

logger = get_logger(__name__)

class Toolbox(ctk.CTkFrame):
    """Toolbox component for drawing tools."""

    def __init__(self, master):
        super().__init__(master)
        self.brush_size = 1
        self.current_tool = "brush"
        self.create_widgets()

    def create_widgets(self):
        """Create and layout the toolbox widgets."""
        print_debug_info()  # Print debug information
        tools = ["brush", "eraser", "dropper", "fill", "zoom"]
        for i, tool in enumerate(tools):
            try:
                icon = ctk.CTkImage(light_image=get_cached_image(f"toolbox/{tool}", (32, 32)), size=(32, 32))
            except FileNotFoundError as e:
                logger.error(f"Error loading icon for {tool}: {str(e)}")
                # Create a default image if the icon can't be loaded
                default_image = Image.new("RGBA", (32, 32), color=(200, 200, 200, 255))
                icon = ctk.CTkImage(light_image=default_image, size=(32, 32))

            button = ctk.CTkButton(
                self,
                image=icon,
                text="",
                width=40,
                height=40,
                command=lambda t=tool: self.set_tool(t)
            )
            button.grid(row=i % 4, column=i // 4, padx=2, pady=2)

        self.brush_size_label = ctk.CTkLabel(self, text=f"Size: {self.brush_size}")
        self.brush_size_label.grid(row=4, column=0, columnspan=2, pady=10)

    def set_tool(self, tool: str):
        """Set the current drawing tool."""
        self.current_tool = tool
        logger.info(f"Current tool: {self.current_tool}")

    def set_brush_size(self, size: int):
        """Set the brush size."""
        self.brush_size = size
        self.brush_size_label.configure(text=f"Size: {self.brush_size}")

    def get_current_tool(self) -> str:
        """Get the current drawing tool."""
        return self.current_tool