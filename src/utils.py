import os
import appdirs
from PIL import Image
from src.logging import get_logger

logger = get_logger(__name__)

def get_project_root():
    """Get the absolute path to the project root."""
    current_path = os.path.abspath(__file__)
    while not os.path.exists(os.path.join(current_path, 'assets')):
        current_path = os.path.dirname(current_path)
        if current_path == os.path.dirname(current_path):  # reached the root directory
            raise FileNotFoundError("Could not find the project root containing 'assets' folder")
    return current_path

def get_cached_image(image_name: str, size: tuple) -> Image.Image:
    """
    Get a cached PNG image from a WebP source, converting if necessary.
    
    :param image_name: Name of the image file (without extension)
    :param size: Desired size of the image as a tuple (width, height)
    :return: PIL Image object
    """
    cache_dir = appdirs.user_cache_dir("PixelScribe")
    cache_asset_dir = os.path.join(cache_dir, "assets")
    os.makedirs(cache_asset_dir, exist_ok=True)
    
    png_path = os.path.join(cache_asset_dir, f"{image_name}.png")
    
    if not os.path.exists(png_path):
        # If PNG doesn't exist in cache, convert from WebP
        project_root = get_project_root()
        webp_path = os.path.join(project_root, "assets", f"{image_name}.webp")
        if not os.path.exists(webp_path):
            logger.error(f"Source image not found: {webp_path}")
            raise FileNotFoundError(f"Source image not found: {webp_path}")
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(png_path), exist_ok=True)
        
        with Image.open(webp_path) as img:
            img = img.resize(size, Image.LANCZOS)
            img.save(png_path, "PNG")
        logger.info(f"Converted and cached image: {png_path}")
    
    return Image.open(png_path).convert("RGBA")

def print_debug_info():
    """Print debug information about file paths."""
    logger.debug(f"Current working directory: {os.getcwd()}")
    logger.debug(f"Project root: {get_project_root()}")
    logger.debug(f"Assets path: {os.path.join(get_project_root(), 'assets')}")
    logger.debug(f"Toolbox assets path: {os.path.join(get_project_root(), 'assets', 'toolbox')}")
    cache_dir = appdirs.user_cache_dir("PixelScribe")
    cache_asset_dir = os.path.join(cache_dir, "assets", "toolbox")
    logger.debug(f"Cache directory: {cache_asset_dir}")
    if os.path.exists(cache_asset_dir):
        for file in os.listdir(cache_asset_dir):
            logger.debug(f"Found cached file: {file}")
    else:
        logger.debug("Cache directory does not exist yet")