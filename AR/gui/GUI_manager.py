import time
import copy

from .draw import *
from hand_detection import HandDetection
from menu import Menu
from apps.app_base import App
from config import PRINT_TIME_OF_DRAWING
from other_utilities import *


class GUImanager:
    def __init__(self):
        self.menu = Menu()
        self.hand_detection = HandDetection()

    def display_GUI(self, image):
        if PRINT_TIME_OF_DRAWING:
            start_time = time.time()

        (image, gestures) = self.hand_detection.process_image(image) # processing image and detecting gestures

        if PRINT_TIME_OF_DRAWING:
            hand_detection_time = time.time()
            hand_detection_diff = hand_detection_time - start_time

        for item in self.menu.items:
            if isinstance(item, App) and item.opened: # if item is app and is opened
                if(self.menu.get_visible()):
                    # when is menu opened, any application can't get a cursor or click event
                    edited_gestures = copy.deepcopy(gestures)
                    edited_gestures.left_hand.clicked = False
                    edited_gestures.left_hand.cursor = Position()
                    edited_gestures.right_hand.clicked = False
                    edited_gestures.right_hand.cursor = Position()

                    item.draw(image, edited_gestures) # drawing app
                else:
                    item.draw(image, gestures) # drawing app
                    
        if PRINT_TIME_OF_DRAWING:
            app_time = time.time()
            app_diff = app_time - hand_detection_time

        self.menu.display_menu(image, gestures)  # drawing menu
        
        if PRINT_TIME_OF_DRAWING:
            menu_time = time.time()
            menu_diff = menu_time - app_time
       
        draw_time_bar(image, self.menu.get_visible())  # drawing time bar

        if gestures.left_hand.cursor.get_array() == (None, None):
            draw_cursor(image, gestures.left_hand.cursor)  # drawing left cursor
        if gestures.right_hand.cursor.get_array() == (None, None):
            draw_cursor(image, gestures.right_hand.cursor)  # drawing right cursor

        #print(f"{gestures.left_hand.cursor.get_array()}  {gestures.left_hand.click_gesture_detected}  {gestures.right_hand.cursor.get_array()}     {gestures.right_hand.click_gesture_detected}")

        if PRINT_TIME_OF_DRAWING:
            print(f"det: {hand_detection_diff*1000}    app: {app_diff*1000}    menu: {menu_diff*1000}        all: {(menu_time - start_time)*1000}")
        return image