import cv2
import numpy as np
from picamera2 import Picamera2

from config import *
from gui.GUI_manager import GUImanager

def main():
    # Kamera
    picam2 = Picamera2()
    
    # Nastavení okna na celoobrazovkový režim
    window_name = 'AR Menu'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    camera_config = picam2.create_still_configuration(main={"size": (W, H)})
    picam2.configure(camera_config)
    picam2.start()


    ui_manager = GUImanager()

    while True:
        # Capture the frame
        image = picam2.capture_array()

        # Convert to RGB (sRGB) if necessary
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

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

        target_width = image.shape[1] // 2

        # Crop the image
        image = image[:, target_width // 2:target_width // 2 + target_width]

        # Draw overlay
        image = ui_manager.display_GUI(image)

        # Add padding to restore height
        image = cv2.copyMakeBorder(image, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT,
                                   value=[0, 0, 0])
        # Duplicate images
        image = np.hstack((image, image))

        # Zobrazení obrazu
        cv2.imshow('AR Menu', image)

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q') or key == ord('Q'):  # ESC nebo 'q' pro ukončení
            break
        if cv2.getWindowProperty('AR Menu', cv2.WND_PROP_VISIBLE) < 1:  # Kontrola zavření okna
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()