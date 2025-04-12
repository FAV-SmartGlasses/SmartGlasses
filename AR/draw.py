import cv2
from gui.button import Button
from gui.toggle_btns import ToggleBtns
#from gui.keyboard import Keyboard
from gui.dropdown import Dropdown
import datetime
from gui.color_manager import *

class Draw:
    @staticmethod
    def cursor(image, cursor_position):
        if cursor_position != (None, None):
            cv2.circle(image, (cursor_position[0], cursor_position[1]), 10, (0, 0, 255), -1)

    @staticmethod
    def rounded_rectangle(image, top_left, bottom_right, radius, color, thickness):
        x1, y1 = top_left
        x2, y2 = bottom_right

        if(thickness == -1):
            # drawing 4 rounded corners (circles) and 2 rectangles
            cv2.circle(image, (x1 + radius, y1 + radius), radius, color, -1)
            cv2.circle(image, (x2 - radius, y1 + radius), radius, color, -1)
            cv2.circle(image, (x1 + radius, y2 - radius), radius, color, -1)
            cv2.circle(image, (x2 - radius, y2 - radius), radius, color, -1)

            cv2.rectangle(image, (x1 + radius, y1), (x2 - radius, y2), color, -1)
            cv2.rectangle(image, (x1, y1 + radius), (x2, y2 - radius), color, -1)
        else:
            # drawing 4 quarter circles
            cv2.ellipse(image, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)  # left upper corner
            cv2.ellipse(image, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)  # right upper corner
            cv2.ellipse(image, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)   # left bottom corner
            cv2.ellipse(image, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)    # right bottom corner

            # drawing 4 lines
            cv2.line(image, (x1 + radius, y1), (x2 - radius, y1), color, thickness)  # upper side
            cv2.line(image, (x1 + radius, y2), (x2 - radius, y2), color, thickness)  # bottom side
            cv2.line(image, (x1, y1 + radius), (x1, y2 - radius), color, thickness)  # left side
            cv2.line(image, (x2, y1 + radius), (x2, y2 - radius), color, thickness)  # right side

    def time_bar(image, h, w, menu_visible):
        # size
        if menu_visible:
            rect_width = 375
        else:
            rect_width = 125 #200
        rect_height = 35 #50 
        
        # position
        x1, y1 = w - rect_width, 0
        x2, y2 = w, rect_height

        radius = 20  # radius of rounded corners

        fill_color = LIGHT_BLUE  # light blue
        font_color = BLACK #WHITE

        overlay = image.copy()

        # drawing left bottom rounded corner
        cv2.circle(overlay, (x1 + radius, y2 - radius), radius, fill_color, -1)
        # drawing the rest of the rectangle
        cv2.rectangle(overlay, (x1, y1), (x2, y2 - radius), fill_color, -1)  # upper part
        cv2.rectangle(overlay, (x1 + radius, y2 - radius), (x2, y2), fill_color, -1)  # bottom part

        cv2.addWeighted(overlay, 1, image, 0, 0, image)

        # getting current time and date
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        current_date = datetime.datetime.now().strftime("%A %d, %B, %Y")

        if menu_visible:
            text = current_date + " " + current_time
        else:
            text = current_time

        # drawing text to rectangle
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
        text_x = w - rect_width + 20 + (rect_width - 40 - text_size[0]) // 2
        text_y = rect_height - (rect_height - text_size[1]) // 2
        cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, font_color, 1, cv2.LINE_AA)