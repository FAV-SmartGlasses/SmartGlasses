import cv2
from gui.UI_manager import UImanager
from config import *
import numpy as np

def main():
    # Kamera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)  # Šířka obrazu
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)  # Výška obrazu

    ui_manager = UImanager()

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image = cv2.flip(image, 1)

        image = cv2.resize(image, (W//2, H//2))

        target_width = image.shape[1] // 2

        #Crop the image
        image = image[:, target_width // 2:target_width // 2 + target_width]

        #Draw overlay
        image = ui_manager.display_UI(image)

        #Duplicate images
        image = np.hstack((image, image))

        # Zobrazení obrazu
        cv2.imshow('AR Menu', image)

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q') or key == ord('Q'):  # ESC nebo 'q' pro ukončení
            break
        if cv2.getWindowProperty('AR Menu', cv2.WND_PROP_VISIBLE) < 1:  # Kontrola zavření okna
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()