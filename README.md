# spritify

This package contains a variety of tools meant to simplify sprite animation(or simply to produce sprite art).
Starting from a non-sprite asset, one can use the functions in the Python program to
produce sprites which may be put together in an animation editor. Additionally, assets may be put into Unity,
for which there is a Spritify shader. After the shader is applied, animations may be acquired easily.

## Functions
Current functions in the Python program are:
- Reduce, which reduces the resolution of an image to be put into a sprite editor,
- Video Pixelation, which takes in a video and outputs either the same video pixelated or all of the pixelated frames,
- Palette Reduction, which takes a sprite and a palette, replacing all pixels' colors with their closest color in the palette, 
- Color Swap, which takes the color in an image to be replaced and the desired color to replace it

## Dependencies
The only dependencies for this program are:
- Pillow
- Numpy
- OpenCV

If you have any questions or would like to collaborate, contact me at sactoa@gmail.com.
