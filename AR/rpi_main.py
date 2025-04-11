import cv2
from gui.UI_manager import UImanager
from config import *
from picamera2 import Picamera2

def main():
    # Kamera
    
    picam2 = Picamera2()
    picam2.start()
    

    ui_manager = UImanager()

    while True:
        # Capture the frame
        image = picam2.capture_array()

        # Convert to RGB (sRGB) if necessary
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image = cv2.flip(image, 1)

        image = ui_manager.display_UI(image)

        #image = cv2.resize(image, (W, H))

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