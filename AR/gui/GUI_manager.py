import copy

from apps.app_base import App
from hand_detection import HandDetection
from menu import Menu
from .draw import *


class GUImanager:
    def __init__(self):
        self.menu = Menu()
        self.hand_detection = HandDetection()

    def display_GUI(self, image):
        (image, gestures) = self.hand_detection.process_image(image) # processing image and detecting gestures

        for item in self.menu.items:
            if isinstance(item, App) and item.opened: # if item is app and is opened
                if self.menu.get_visible():
                    # when is menu opened, any application can't get a cursor or click event
                    edited_gestures = copy.deepcopy(gestures)
                    edited_gestures.left_hand.clicked = False
                    edited_gestures.left_hand.cursor = Position()
                    edited_gestures.right_hand.clicked = False
                    edited_gestures.right_hand.cursor = Position()

                    item.draw(image, edited_gestures) # drawing app
                else:
                    item.draw(image, gestures) # drawing app

        self.menu.display_menu(image, gestures)  # drawing menu
       
        draw_time_bar(image, self.menu.get_visible())  # drawing time bar

        if gestures.left_hand.cursor.get_array() == (None, None):
            draw_cursor(image, gestures.left_hand.cursor)  # drawing left cursor
        if gestures.right_hand.cursor.get_array() == (None, None):
            draw_cursor(image, gestures.right_hand.cursor)  # drawing right cursor

        #print(f"{gestures.left_hand.cursor.get_array()}  {gestures.left_hand.click_gesture_detected}  {gestures.right_hand.cursor.get_array()}     {gestures.right_hand.click_gesture_detected}")

        image = add_transparent_ring(image)

        return image