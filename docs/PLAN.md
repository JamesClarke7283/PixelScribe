# Pixel Scribe Plan
Its meant to be simple to use, so we shall start with the basics.

Canvas is implemented in pygame, rest of the components are written with Customtkinter.

We start with a Palette on the left hand side, written in customtkinter, in the centre of the screen is the Canvas.
You have a brush size set to 1 pixel, and the default pixel grid is 64x64 pixels.

You can use the mouse wheel to resize the square brush (make sure to make it modular so you can have different brush types later).

We have a Brush tool, Eraser, Dropper (Sets the palette colour to the currently clicked on pixel), and Fill(The bucket symbol, it sets the currently selected colour and all colours exactly adjacent to it with the same colour, to the palette colour)

The background of the canvas starts as filled in white, and behind it is transparent (represented by a checkerboard pattern)

Please for the toolbox point the assets for each "tool" to the ./assets/toolbox, as the prefix, and all tools will just be instanciated with a different .png file, the assets in the ./assets folder will be mirrored to the cache folder for PixelScribe using the appdirs package, so we convert the ./assets from webp to png nicely. Make sure to resize the icons which will be 1024x1024, to a suitable size like 32x32 in the toolbox palette.

This should give us a basic interface to do pixelart, dont worry about saving just yet. Just make sure to put all logic representations of the image in the src/core folder under a .py file, and the ui and pygame elements in the components folder under seperate .py files.
