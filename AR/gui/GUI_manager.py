import time

from .draw import *
from hand_detection import HandDetection
from menu import Menu
from apps.app_base import App


class GUImanager:
    def __init__(self):
        self.menu = Menu()
        self.hand_detection = HandDetection()

    def display_GUI(self, image):
        start_time = time.time()

        h, w, _ = image.shape
        (
            image, 
            left_click_gesture_detected, right_click_gesture_detected, 
            swipe_gesture_detected, 
            left_cursor_position, right_cursor_position
         ) = self.hand_detection.process_image(image, w, h) # processing image and detecting gestures
        
        hand_detection_time = time.time()
        hand_detection_diff = hand_detection_time - start_time

        for item in self.menu.items:
            if isinstance(item, App) and item.opened: # if item is app and is opened
                if(self.menu.get_visible()):
                    item.draw(image,
                          False, False, 
                          (None, None), (None, None)) # drawing app
                else:
                    item.draw(image,
                          left_click_gesture_detected, right_click_gesture_detected, 
                          left_cursor_position, right_cursor_position) # drawing app
                    
        app_time = time.time()
        app_diff = app_time - hand_detection_time

        self.menu.display_menu(image, 
                               left_click_gesture_detected, right_click_gesture_detected,
                               swipe_gesture_detected, 
                               left_cursor_position, right_cursor_position)  # drawing menu
        
        menu_time = time.time()
        menu_diff = menu_time - app_time
       
        draw_time_bar(image, h, w, self.menu.get_visible())  # drawing time bar

        draw_cursor(image, left_cursor_position)  # drawing left cursor
        draw_cursor(image, right_cursor_position)  # drawing right cursor

        print(f"det: {hand_detection_diff*1000}    app: {app_diff*1000}    menu: {menu_diff*1000}        all: {(menu_time - start_time)*1000}")
        return image