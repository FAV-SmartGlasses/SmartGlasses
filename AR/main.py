import cv2
import numpy as np
import time

from config import *
from gui.GUI_manager import GUImanager
from camera_manager import CameraManager


def main():
    cv2.setUseOptimized(True)
    
    # Camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)  # Image width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)  # Image height

    ui_manager = GUImanager()
    camera_manager = CameraManager(scale_down=SCALE_DOWN, show_fps=SHOW_FPS, two_eyes=TWO_EYES)

    while True:
        success, image = cap.read()
        if not success:
            break

        image, resized_w, resized_h = camera_manager.process_frame(image)
        image = cv2.flip(image, 1)  # Flip the image horizontally
        image = ui_manager.display_GUI(image)

        if TWO_EYES:
            image = camera_manager.make_two_eye_view(image, resized_w, resized_h)

        camera_manager.calculate_fps()
        camera_manager.display_fps(image, resized_w, resized_h)

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