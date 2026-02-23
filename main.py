import cv2
import os
from pathlib import Path

import tkinter as tk
from tkinter import filedialog

import shutil

drawing = False
start_x, start_y = -1, -1
rectangles = []

original_image = None
display_image = None
current_image_path = None
input_dir = None
SESSION_FILE = Path(__file__).parent / "last_session.txt"



def mouse_callback(event, x, y, flags, param):
    global drawing, start_x, start_y, display_image

    # First click → start rectangle
    if event == cv2.EVENT_LBUTTONDOWN and not drawing:
        drawing = True
        start_x, start_y = x, y

    # Mouse move → show preview
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        display_image = original_image.copy()

        # draw existing rectangles
        for (x1, y1, x2, y2) in rectangles:
            cv2.rectangle(display_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # draw preview rectangle
        cv2.rectangle(display_image, (start_x, start_y), (x, y), (255, 0, 0), 2)

    # Second click → finish rectangle
    elif event == cv2.EVENT_LBUTTONDOWN and drawing:
        drawing = False

        x1, x2 = sorted([start_x, x])
        y1, y2 = sorted([start_y, y])

        rectangles.append((x1, y1, x2, y2))

        display_image = original_image.copy()

        # redraw all rectangles
        for (rx1, ry1, rx2, ry2) in rectangles:
            cv2.rectangle(display_image, (rx1, ry1), (rx2, ry2), (0, 255, 0), 2)



def save_crops():
    base_name = current_image_path.stem

    output_dir = input_dir.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if not rectangles:
        destination = output_dir / current_image_path.name
        shutil.copy2(current_image_path, destination)
        print(f"Copied full image: {destination}")
        return

    for idx, (x1, y1, x2, y2) in enumerate(rectangles, start=1):
        crop = original_image[y1:y2, x1:x2]
        if crop.size == 0:
            continue

        filename = f"{base_name}_{idx:02d}.jpg"
        output_path = output_dir / filename

        cv2.imwrite(str(output_path), crop)
        print(f"Saved: {output_path}")



def load_image(path):
    global original_image, display_image, rectangles, current_image_path

    rectangles = []
    current_image_path = path

    original_image = cv2.imread(str(path))

    if original_image is None:
        print(f"Could not load image: {path}")
        return

    display_image = original_image.copy()
    update_window_title()



def update_window_title():
    window_title = f"Image Region Extractor - {current_image_path.name}"
    cv2.setWindowTitle("Image", window_title)



def choose_folder():
    root = tk.Tk()
    root.withdraw()

    folder_selected = filedialog.askdirectory(
        title="Select folder with images"
    )

    root.destroy()

    return folder_selected



def rotate_image(direction):
    global original_image, display_image, rectangles

    if direction == "left":
        original_image = cv2.rotate(original_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    elif direction == "right":
        original_image = cv2.rotate(original_image, cv2.ROTATE_90_CLOCKWISE)

    rectangles.clear()
    display_image = original_image.copy()



def overwrite_original():
    if current_image_path is None:
        return

    cv2.imwrite(str(current_image_path), original_image)
    print(f"Overwritten: {current_image_path.name}")



def save_session(image_path):
    with open(SESSION_FILE, "w") as f:
        f.write(image_path.name)



def load_session():
    if not Path(SESSION_FILE).exists():
        return None

    with open(SESSION_FILE, "r") as f:
        return f.read().strip()



def main():
    global display_image, input_dir

    folder = choose_folder()

    if not folder:
        print("No folder selected.")
        return

    input_dir = Path(folder)

    last_image_name = load_session()


    image_paths = sorted(
        [p for p in input_dir.iterdir() if p.suffix.lower() in [".jpg", ".jpeg", ".png"]]
    )

    if not image_paths:
        print("No images found.")
        return

    index = 0

    if last_image_name:
        for i, path in enumerate(image_paths):
            if path.name == last_image_name:
                index = i
                break


    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", mouse_callback)
    load_image(image_paths[index])


    while True:
        cv2.imshow("Image", display_image)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            save_session(image_paths[index])
            break

        elif key == ord("l"):
            rotate_image("left")

        elif key == ord("r"):
            rotate_image("right")

        elif key == ord("s"):
            save_crops()

        elif key == ord("c"):
            rectangles.clear()
            display_image = original_image.copy()

        elif key in (8, 127):  # Backspace / Delete
            if rectangles:
                rectangles.pop()
                display_image = original_image.copy()

                for (rx1, ry1, rx2, ry2) in rectangles:
                    cv2.rectangle(display_image, (rx1, ry1), (rx2, ry2), (0, 255, 0), 2)
                
                print("Last rectangle removed.")

        elif key == ord("n"):
            save_crops()

            index += 1
            if index >= len(image_paths):
                print("No more images.")
                break

            next_image = image_paths[index]
            save_session(next_image)
            load_image(next_image)


        elif key == ord("w"):
            overwrite_original()

    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
