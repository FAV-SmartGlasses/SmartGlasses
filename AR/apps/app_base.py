from abc import abstractmethod

import cv2
import numpy as np
import math

from hand_detection_models import *
from menu_items import MenuItem
from other_utilities import *
from config import r


def is_hovered(cursor_x, cursor_y, x1, y1, x2, y2):
    return x1 <= cursor_x <= x2 and y1 <= cursor_y <= y2


def calculate_hover_region(center, length, offset, is_vertical=False):
    """
    Calculate a rectangular hover region based on a center coordinate, length, and offset.
    If is_vertical is True, the region is vertical; otherwise, it is horizontal.
    """
    if is_vertical:
        return (
            offset,
            center - length // 2,
            offset + 20,
            center + length // 2
        )
    else:
        return (
            center - length // 2,
            offset,
            center + length // 2,
            offset + 20
        )


def is_within_distance(point1: Position, point2: Position, max_distance: float) -> bool:
    distance = math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
    return distance <= max_distance


class App(MenuItem):
    @abstractmethod
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.opened = False
        self._position: Position = Position(0, 0)
        self._size: Size = Size(400, 400)
        self.pages = []
        self.current_page = 0

    def add_page(self, page):
        self.pages.append(page)

    def switch_page(self, page_index):
        if 0 <= page_index < len(self.pages):
            self.current_page = page_index
        else:
            print(f"Invalid page index: {page_index}")

    def check_fist_gesture(self, gestures: DetectionModel):
        if (gestures.right_hand.last_wrist_position.get_array() != (None,None) and 
            gestures.right_hand.fist == True and
            gestures.right_hand.wrist_position.get_array() != (None,None)):

            wrist_diff = get_difference_between_positions(gestures.right_hand.last_wrist_position, gestures.right_hand.wrist_position)
            new_position = get_sum_of_positions(self._position, wrist_diff)

            if is_within_distance(new_position, self._position, r):
                self._position = new_position

    def resize(self, gestures: DetectionModel, resize_w: bool, resize_h: bool):
        cursor_diff = get_difference_between_positions(gestures.right_hand.last_cursor_position, gestures.right_hand.cursor)
        if resize_w:
            self.set_width(get_sum_of_size_and_position(self._size, cursor_diff).w)
        if resize_h:
            self.set_height(get_sum_of_size_and_position(self._size, cursor_diff).h)

    def draw_lines(self, image: np.ndarray, gestures: DetectionModel):
        """
        Draws shorter lines on the right and bottom sides of the application and a circle in the bottom-right corner.
        If the cursor (left or right) hovers over these elements, they become thicker or change color.
        The circle is only drawn if the app type is FreeResizeApp.
        Additionally, handles resizing logic based on clicks.
        """
        # Get cursor positions for both hands
        cursors = [
            gestures.right_hand.cursor.get_array(),
            gestures.left_hand.cursor.get_array()
        ]

        # Filter out invalid cursor positions
        cursors = [pos for pos in cursors if pos != (None, None)]

        if not cursors:
            return

        app_x, app_y = self._position.x, self._position.y
        app_width, app_height = self._size.w, self._size.h

        # Define line and circle properties
        default_thickness = 10
        hover_thickness = 20
        line_length = 60  # Shorter line length
        circle_radius = 20
        circle_thickness = 3
        default_color = (0, 255, 0)  # Green color
        hover_color = (255, 0, 0)  # Red color

        # Initialize hover states
        right_line_thickness = default_thickness
        bottom_line_thickness = default_thickness
        circle_color = default_color

        # Initialize resize flags
        resize_w = False
        resize_h = False

        # Define hover regions for right line and bottom line using the updated helper function
        right_line_region = calculate_hover_region(app_y + app_height // 2, line_length, app_x + app_width, is_vertical=True)
        bottom_line_region = calculate_hover_region(app_x + app_width // 2, line_length, app_y + app_height, is_vertical=False)

        # Check hover and click for each cursor
        right_x = app_x + app_width
        bottom_line_bottom_y = app_y + app_height
        for x, y in cursors:
            # Check if cursor is hovering over the right line
            if is_hovered(x, y, *right_line_region):
                right_line_thickness = hover_thickness
                if gestures.right_hand.clicked:
                    resize_w = True
                    resize_h = False

            # Check if cursor is hovering over the bottom line
            if is_hovered(x, y, *bottom_line_region):
                bottom_line_thickness = hover_thickness
                if gestures.right_hand.clicked:
                    resize_w = False
                    resize_h = True

            # Check if cursor is hovering over the circle
            circle_center = (right_x - circle_radius - 10, bottom_line_bottom_y - circle_radius - 10)
            if (x - circle_center[0]) ** 2 + (y - circle_center[1]) ** 2 <= circle_radius ** 2:
                circle_color = hover_color
                circle_thickness = -1 # Make the circle filled
                if gestures.right_hand.clicked:
                    resize_w = True
                    resize_h = True

        # Draw the right line
        cv2.line(
            image,
            (right_x, app_y + app_height // 2 - line_length // 2),
            (right_x, app_y + app_height // 2 + line_length // 2),
            default_color,
            right_line_thickness
        )

        # Draw the bottom line
        cv2.line(
            image,
            (app_x + app_width // 2 - line_length // 2, bottom_line_bottom_y),
            (app_x + app_width // 2 + line_length // 2, bottom_line_bottom_y),
            default_color,
            bottom_line_thickness
        )

        # Draw the circle in the bottom-right corner only if the app is FreeResizeApp
        if isinstance(self, FreeResizeApp):
            circle_center = (right_x - circle_radius - 10, bottom_line_bottom_y - circle_radius - 10)
            cv2.circle(
                image,
                circle_center,
                circle_radius,
                circle_color,
                circle_thickness
            )

        # Perform resizing if applicable
        if resize_w or resize_h:
            self.resize(gestures, resize_w, resize_h)

    def clicked(self):
        super().clicked()
        if self.opened:
            self.close()
        else:
            self.launch()

    def launch(self):
        self.opened = True

    def close(self):
        self.opened = False

    def set_width(self, w):
        self._size.w = w

    def set_height(self, h):
        self._size.h = h

    def draw(self, image: np.ndarray, gestures: DetectionModel):
        self.draw_lines(image, gestures)

class FixedAspectApp(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        
        self.aspect_ratio: int | None = None

    @abstractmethod
    def compute_aspect_ratio(self):
        raise NotImplementedError

    def set_width(self, w):
        h = int(w / self.aspect_ratio)
        self._size = Size(w, h)

    def set_height(self, h):
        w = int(h * self.aspect_ratio)
        self._size = Size(w, h)


class FreeResizeApp(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)

    def set_size(self, w, h):
        self._size = Size(w, h)

    def set_width(self, w):
        self._size.w = w

    def set_height(self, h):
        self._size.h = h