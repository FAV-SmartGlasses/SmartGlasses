import cv2
from hand_detection import HandDetection
from menu import Menu

# Kamera
cap = cv2.VideoCapture(1)

menu_visible = False
current_selection = 0

hand_detection = HandDetection()
menu = Menu()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    h, w, _ = image.shape

    image, menu_visible, current_selection = hand_detection.process_image(image, w, h, menu_visible, current_selection)

    image = menu.display_menu(image, current_selection, menu_visible, h)

    # Zobrazení obrazu
    cv2.imshow('VR Menu', image)

    # Detekce stisknutí klávesy pro otevření/zavření menu
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC pro ukončení
        break

cap.release()
cv2.destroyAllWindows()