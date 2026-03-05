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
>
>python main.py

fyi last_session is saved in the script's dir

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

Expected output:

Saved: /Users/kuba/Desktop/output/00014_IMG_20260207_123302_02.jpg

Image discarded.

Last rectangle removed.

Last rectangle removed.

Saved: /Users/kuba/Desktop/output/00016_IMG_20260207_123446_01.jpg

Saved: /Users/kuba/Desktop/output/00016_IMG_20260207_123446_02.jpg

Saved: /Users/kuba/Desktop/output/00016_IMG_20260207_123446_03.jpg

Saved: /Users/kuba/Desktop/output/00016_IMG_20260207_123446_04.jpg

Saved: /Users/kuba/Desktop/output/00016_IMG_20260207_123446_05.jpg

Copied full image: /Users/kuba/Desktop/output/00017_IMG_20260207_123449.jpg

Saved: /Users/kuba/Desktop/output/00018_IMG_20260207_123456_01.jpg

Saved: /Users/kuba/Desktop/output/00018_IMG_20260207_123456_02.jpg

Copied full image: /Users/kuba/Desktop/output/00019_IMG_20260207_123458.jpg

Copied full image: /Users/kuba/Desktop/output/00020_IMG_20260207_123508.jpg

Overwritten: 00021_IMG_20260207_123524.jpg
