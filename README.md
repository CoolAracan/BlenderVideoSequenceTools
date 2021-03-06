# BlenderVideoSequenceTools
____

A collection of tools for Blender's video sequence tool. When confronted with the task of compiling a video with a lot of still images in Blender, I got the idea for these tools. They should facilitate the video creation process.

The tools consist of two major components:
- An importer for videos and images alike in sequential order with the file name as clip name.
- A variety of modifiers for panning/zooming and blurring the images comfortably

## Installation
As usual, just download the python-script and install it via Blender.
A good documentation about this can be found here: [Official documentation](https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html#install-the-add-on)

The addon category is "Sequencer".

## Importing sequences of images and videos

https://user-images.githubusercontent.com/98447390/157609115-15cc8171-ba7f-44e9-a0af-1d7c5d3d9ace.mp4

To import images and movies alike, go to the video editing view, click "Add" and select "Image/Movie sequence".
A file dialog will pop up in which you can select all files to be imported.

Following options are available:

### Number of frames per image
This value influences the length of any single image clip. The value given is in frames. The length in time therefore depends on the project's frame rat. Movie clips are not altered and will be inserted in full length.

### Zoom factor
The zoom factor determines how far an image is zoomed into for animation. It is given as a fraction of image size and should not be less than 1.

### Speed factor
The speed factor determines how fast an animation for an image is set. A value of 1 equals an animation length as long as the clip. It can extended or shortened as desired.

### Linear interpolation
If linear interpolation is enabled, animations will not have a smooth start and end, but instead start with constant animation speed.

### Insert at current frame
If enabled, images and movies will be inserted after the currently selected frame.


## Adding pan/zoom and blur effects to images

https://user-images.githubusercontent.com/98447390/157609188-e4187710-bc3b-43a8-942a-d86df9869038.mp4

To make a sequence of stills a bit more dynamic, some effects can be applied to them. When they where imported with the import tool, these effects, are already randomly applied. If an effect doesn't suite your need, you can clear it and afterwards apply one to your liking. They can be accessed in the sequencer by clicking "Image", selecting "Pan/Zoom tools" and chosing the respective tool.

Effects are applied to a single marked clip.

Options are zoom factor and speed, as described above.

- ### Clear
  Clears the image clip from all animations. Be careful, not only the animations created with this tool, but all animations will be lost.

- ### Zoom in
  A simple zoom in effect. 

- ### Zoom out
  A simple zoom out effect.

- ### Top to bottom pan
  Image is panned from top to bottom.

- ### Left to right pan
  Image is panned from left to right.

- ### Right to left pan
  Image is panned from right to left.

- ### Top left to bottom right pan
  Image is panned diagonally from top left to bottom right corner.

- ### Top right to bottom left pan
  Image is panned diagonally from top right to bottom left corner.

- ### Add blurred background
  The blurred background effect is especially for portrait images/movies. To make the black bars left and rigth a bit more pleasant, the image is enlarged and blurred in the background.

## Closing remarks
As I noticed that Blender VSE does only use one CPU, I strongly advise you to use [Parallel Renderer by Krzysztof Trzci??ski](https://github.com/elmopl/ktba/blob/master/scripts/addons/parallel_render.py).

I am always open for honest feedback, merge requests and ideas for improving my code and this tool.
Please be kind as this is my first open source project :)

## Credits
Pictures and videos in the sample videos taken from wikimedia.
All images and videos are under [CC0-by-SA](https://creativecommons.org/licenses/by-sa/4.0/deed.en).

- [Blackberries by Ivar Leidus](https://commons.wikimedia.org/wiki/File:Blackberries_(Rubus_fruticosus).jpg)
- [Brown thrasher in CP by Rhododendrites](https://commons.wikimedia.org/wiki/File:Blackberries_(Rubus_fruticosus).jpg)
- [Honey bees drinking water by Goovaeh8fot6yugh](https://commons.wikimedia.org/wiki/File:Blackberries_(Rubus_fruticosus).jpg)
- [Samuel Dunn Wall Map of the World in Hemispheres by Thomas Kitchin](https://commons.wikimedia.org/wiki/File:Blackberries_(Rubus_fruticosus).jpg)
- [Four ladies wearing a yukata in front of the North Gate of Kiyomizu-dera temple Kyoto Japan by Basile Morin](https://commons.wikimedia.org/wiki/File:Blackberries_(Rubus_fruticosus).jpg)
- [Mother and baby sperm whale by Gabriel Barathieu](https://commons.wikimedia.org/wiki/File:Blackberries_(Rubus_fruticosus).jpg)

Videos were created using OBS Studio and converted using ffmpeg.
