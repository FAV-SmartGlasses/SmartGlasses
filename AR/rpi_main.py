import cv2
from picamera2 import Picamera2

from camera_manager import CameraManager
from config import *
from gui.GUI_manager import GUImanager


def main():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (W, H)})
    picam2.configure(camera_config)
    picam2.start()

    window_name = 'AR Menu'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    ui_manager = GUImanager()
    camera_manager = CameraManager(scale_down=SCALE_DOWN, show_fps=SHOW_FPS, two_eyes=TWO_EYES)

    while True:
        image = picam2.capture_array()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image, resized_w, resized_h = camera_manager.process_frame(image)
        image = ui_manager.display_GUI(image)

        image = camera_manager.make_two_eye_view(image, resized_w, resized_h)

        camera_manager.calculate_fps()
        camera_manager.display_fps(image, resized_w, resized_h)

        cv2.imshow('AR Menu', image)

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q') or key == ord('Q'):
            break
        if cv2.getWindowProperty('AR Menu', cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()