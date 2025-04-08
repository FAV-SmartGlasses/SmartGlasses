from menu import Menu
from hand_detection import HandDetection
import datetime
import cv2
from Apps.calculator import Calculator, App

class UImanager:
    def __init__(self):
        self.menu = Menu()
        self.hand_detection = HandDetection()
        self.calculator = Calculator("Calculator", "Calculator", "Plus.png")
        self.calculator.opened = True

    def display_UI(self, image):
        h, w, _ = image.shape

        image, click_gesture_detected, swipe_gesture_detected, cursor_position = self.hand_detection.process_image(image, w, h)

        self.menu.display_menu(image, click_gesture_detected, swipe_gesture_detected, cursor_position)  # Vykreslení menu

        for item in self.menu.items:
            if isinstance(item, App) and item.opened: # and isinstance(item, Calculator):
                item.draw(image, w, h, click_gesture_detected, cursor_position)

        #self.calculator.draw(image, w, h, click_gesture_detected, cursor_position)  # Vykreslení aplikací
       
        self.draw_time_bar(image, h, w, self.menu.get_visible())  # Vykreslení bubliny s časem

        self.draw_cursor(image, cursor_position)  # Vykreslení kurzoru

        return image
    

    def draw_cursor(self, image, cursor_position):
        if cursor_position != (None, None):
            cv2.circle(image, (cursor_position[0], cursor_position[1]), 10, (0, 0, 255), -1)

    def draw_time_bar(self, image, h, w, menu_visible):
        # Souřadnice a velikost obdélníku
        if(menu_visible):
            rect_width = 375
        else:
            rect_width = 125 #200
        rect_height = 35 #50 
        
        x1, y1 = w - rect_width, 0
        x2, y2 = w, rect_height

        radius = 20  # Poloměr zaoblení rohu

        # Barva obdélníku
        fill_color = (248, 255, 145)  # Světle modrá
        font_color = (0, 0, 0) #(255, 255, 255)

        # Kreslení obdélníku s levým dolním rohem zaobleným
        overlay = image.copy()

        # levý dolní zaoblený roh
        cv2.circle(overlay, (x1 + radius, y2 - radius), radius, fill_color, -1)  # Levý dolní roh
        # zbytek obdélníku
        cv2.rectangle(overlay, (x1, y1), (x2, y2 - radius), fill_color, -1)  # Horní část obdélníku
        cv2.rectangle(overlay, (x1 + radius, y2 - radius), (x2, y2), fill_color, -1)  # Spodní část obdélníku

        cv2.addWeighted(overlay, 1, image, 0, 0, image)

        # Získání aktuálního času a datumu
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        current_date = datetime.datetime.now().strftime("%A %d, %B, %Y")

        if(menu_visible):
            text = current_date + " " + current_time
        else:
            text = current_time

        # Vykreslení času do obdélníku
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
        text_x = w - rect_width + 20 + (rect_width - 40 - text_size[0]) // 2
        text_y = rect_height - (rect_height - text_size[1]) // 2
        cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, font_color, 1, cv2.LINE_AA)