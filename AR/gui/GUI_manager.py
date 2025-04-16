from gui.draw import *
from hand_detection import HandDetection
from menu import Menu
from Apps.app_base import App


class GUImanager:
    def __init__(self):
        self.menu = Menu()
        self.hand_detection = HandDetection()

    def display_GUI(self, image):
        h, w, _ = image.shape

        (
            image, 
            left_click_gesture_detected, right_click_gesture_detected, 
            swipe_gesture_detected, 
            left_cursor_position, right_cursor_position
         ) = self.hand_detection.process_image(image, w, h) # processing image and detecting gestures

        self.menu.display_menu(image, 
                               left_click_gesture_detected, right_click_gesture_detected,
                               swipe_gesture_detected, 
                               left_cursor_position, right_cursor_position)  # drawing menu

        print(left_cursor_position, right_cursor_position)

        for item in self.menu.items:
            if isinstance(item, App) and item.opened: # if item is app and is opened
                #print(left_cursor_position, right_cursor_position)
                item.draw(image, w, h, 
                          left_click_gesture_detected, right_click_gesture_detected, 
                          left_cursor_position, right_cursor_position) # drawing app
                #print(left_cursor_position, right_cursor_position)
       
        draw_time_bar(image, h, w, self.menu.get_visible())  # drawing time bar

        draw_cursor(image, left_cursor_position)  # drawing left cursor
        draw_cursor(image, right_cursor_position)  # drawing right cursor

        return image