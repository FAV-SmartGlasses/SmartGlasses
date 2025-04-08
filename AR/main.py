import cv2
from UI_manager import UImanager
#from menu import Menu

# Kamera
cap = cv2.VideoCapture(1)

menu_visible = False
current_selection = 0

ui_manager = UImanager()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = cv2.flip(image, 1)

    image = ui_manager.display_UI(image)

    # Zobrazení obrazu
    cv2.imshow('AR Menu', image)

    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q') or key == ord('Q'):  # ESC nebo 'q' pro ukončení
        break
    if cv2.getWindowProperty('AR Menu', cv2.WND_PROP_VISIBLE) < 1:  # Kontrola zavření okna
        break

cap.release()
cv2.destroyAllWindows()