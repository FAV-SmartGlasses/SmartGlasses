from menu import Menu
from hand_detection import HandDetection
import datetime
import cv2
from Apps.calculator import Calculator
import menu_items
from draw import Draw

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

        for item in self.menu.items:
            if isinstance(item, menu_items.App) and item.opened: # if item is app and is opened
                item.draw(image, w, h, 
                          left_click_gesture_detected, right_click_gesture_detected, 
                          left_cursor_position, right_cursor_position) # drawing app
       
        Draw.time_bar(image, h, w, self.menu.get_visible())  # drawing time bar

        Draw.cursor(image, left_cursor_position)  # drawing left cursor
        Draw.cursor(image, right_cursor_position)  # drawing right cursor

        return image

    def draw_gui_objects(self, image, objects, cursor_position, click_gesture_detected):
        for obj in objects:
            match obj.__class__:
                case Button:
                    is_hovered = self.is_cursor_in_rect(cursor_position, obj.rect)
                    obj.draw(image, is_hovered)

    def is_cursor_in_rect(self, position, rect):
        if position  == (None, None) or rect  == ((None, None),(None, None)):
            return False
        
        x1, y1, x2, y2 = rect
        if x1 <= position[0] <= x2 and y1 <= position[1] <= y2:
            return True
        
        return False