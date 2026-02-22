import cv2
import os
from pathlib import Path

drawing = False
start_x, start_y = -1, -1
rectangles = []

original_image = None
display_image = None
current_image_path = None


# def mouse_callback(event, x, y, flags, param):
#     global drawing, start_x, start_y, display_image

#     if event == cv2.EVENT_LBUTTONDOWN:
#         drawing = True
#         start_x, start_y = x, y

#     elif event == cv2.EVENT_MOUSEMOVE and drawing:
#         display_image = original_image.copy()
#         for (x1, y1, x2, y2) in rectangles:
#             cv2.rectangle(display_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.rectangle(display_image, (start_x, start_y), (x, y), (255, 0, 0), 2)

#     elif event == cv2.EVENT_LBUTTONUP:
#         drawing = False
#         x1, x2 = sorted([start_x, x])
#         y1, y2 = sorted([start_y, y])

#         rectangles.append((x1, y1, x2, y2))

#         cv2.rectangle(display_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

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
    output_dir = current_image_path.parent

    for idx, (x1, y1, x2, y2) in enumerate(rectangles, start=1):
        crop = original_image[y1:y2, x1:x2]
        if crop.size == 0:
            continue

        filename = f"{base_name}_{idx:02d}.jpg"
        output_path = output_dir / filename
        cv2.imwrite(str(output_path), crop)
        print(f"Saved: {filename}")


def load_image(path):
    global original_image, display_image, rectangles, current_image_path

    rectangles = []
    current_image_path = path

    original_image = cv2.imread(str(path))
    display_image = original_image.copy()


def main():
    global display_image

    folder = input("Enter folder path with images: ")
    image_paths = sorted(
        [p for p in Path(folder).iterdir() if p.suffix.lower() in [".jpg", ".jpeg", ".png"]]
    )

    if not image_paths:
        print("No images found.")
        return

    index = 0
    load_image(image_paths[index])

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", mouse_callback)

    while True:
        cv2.imshow("Image", display_image)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            break

        elif key == ord("s"):
            save_crops()

        elif key == ord("r"):
            rectangles.clear()
            display_image = original_image.copy()

        elif key == ord("n"):
            save_crops()
            index += 1
            if index >= len(image_paths):
                print("No more images.")
                break
            load_image(image_paths[index])

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
