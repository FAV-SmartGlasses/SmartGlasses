import cv2
from gui.UI_manager import UImanager
from config import *
from picamera2 import Picamera2
import numpy as np

def main():
    # Kamera
    
    picam2 = Picamera2()
    
    # Nastavení okna na celoobrazovkový režim
    window_name = 'AR Menu'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    camer_config = picam2.create_still_configuration(main={"size": (W, H)})
    picam2.configure(camer_config)
    picam2.start()


    ui_manager = UImanager()

    while True:
        # Capture the frame
        image = picam2.capture_array()

        # Convert to RGB (sRGB) if necessary
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image = cv2.flip(image, 1)

        target_width = image.shape[1] // 2

        # Crop the image
        image = image[:, target_width // 2:target_width // 2 + target_width]

        # Draw overlay
        image = ui_manager.display_UI(image)

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