import cv2
from gui.GUI_manager import GUImanager
from config import *
import numpy as np

SCALE_DOWN = 5

def main():
    # Camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)  # Image width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)  # Image height

    ui_manager = GUImanager()

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        original_h, original_w = image.shape[:2]

        # Resize image
        resized_image = cv2.resize(image, (original_w - original_w//SCALE_DOWN, original_h - original_h//SCALE_DOWN))
        resized_h, resized_w = resized_image.shape[:2]

        # Calculate padding needed
        pad_top = (original_h - resized_h) // 2
        pad_bottom = original_h - resized_h - pad_top
        pad_left = (original_w - resized_w) // 2
        pad_right = original_w - resized_w - pad_left

        # Add padding to restore original width
        image = cv2.copyMakeBorder(resized_image, 0, 0, pad_left, pad_right, cv2.BORDER_CONSTANT,
                                   value=[0, 0, 0])

        image = cv2.flip(image, 1)

        target_width = image.shape[1] // 2

        # Crop the image
        image = image[:, target_width // 2:target_width // 2 + target_width]

        # Draw overlay
        image = ui_manager.display_GUI(image)

        if TWO_EYES:
            # Add padding to restore height
            image = cv2.copyMakeBorder(image, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT,
                                    value=[0, 0, 0])
            # Duplicate images
            image = np.hstack((image, image))

        # Display the image
        cv2.imshow('AR Menu', image)

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q') or key == ord('Q'):  # ESC or 'q' to exit
            break
        if cv2.getWindowProperty('AR Menu', cv2.WND_PROP_VISIBLE) < 1:  # Check if the window is closed
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()