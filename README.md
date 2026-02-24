# ImageRegionExtractor
ImageRegionExtractor is a desktop tool that allows users to manually select multiple rectangular regions from images and automatically saves each selected area as a separate image file with sequential filenames, streamlining the processing of large image collections.

install python-tk to include tcl-tk package that offers window GUI management:
>brew install python-tk@3.14

create and activate virtual env to install opencv locally in a project dir:
>python3 -m venv venv
>
>source venv/bin/activate

confirm that you're using python and pip from venv
>which python3
>
>which pip

install opencv and run program
>pip install opencv-python
>python main.py


>ESC - point "last_session" file to a current image (with no rectangles) and quit,
>
>n - extract crops as new images, go next, and point "last_session" to an opened image,
>
>c - clear rectangles, 
>
>backspace / delete - undo last rectangle,
>
>l - rotate left,
>
>r - rotate right,
>
>w - overwrite original image,
>
>d - discard image.

last_session is saved in the script's dir
