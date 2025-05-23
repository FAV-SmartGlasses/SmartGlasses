import datetime
import cv2
import numpy as np

from .color_manager import *
from other_utilities import Position
from config import r, r2, alpha_value


def draw_cursor(image, cursor_position):
    if cursor_position.get_array() != (None, None):
        cv2.circle(image, (cursor_position.x, cursor_position.y), 10, (0, 0, 255), -1)

def draw_gui_objects(self, image, objects, cursor_position, click_gesture_detected):
    for obj in objects:
        match obj.__class__:
            case Button:
                is_hovered = self.is_cursor_in_rect(cursor_position, obj.rect)
                obj.draw(image, is_hovered)

def is_cursor_in_rect(position: Position, rect):
    if position.get_array() == (None, None) or rect  == (None, None, None, None):
        return False
    
    x1, y1, x2, y2 = rect
    if x1 <= position.x <= x2 and y1 <= position.y <= y2:
        return True
    
    return False

def draw_rounded_rectangle(image: np.ndarray, top_left: tuple[int, int], bottom_right: tuple[int, int], radius: int, color: tuple[int, int, int], thickness: int):
    x1, y1 = top_left
    x2, y2 = bottom_right

    if thickness == -1:
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

def draw_time_bar(image, menu_visible):
    h, w, _ = image.shape

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

    fill_color = get_nice_color()
    font_color = get_font_color()

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

def add_transparent_ring(image):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)

    # Spočítat poloměr tak, aby přetékal ven
    outer_radius = int(np.hypot(w, h))

    # Tloušťka bude rozdíl mezi vnějším a vnitřním poloměrem
    thickness = outer_radius - r2

    # Vykreslit černý prstenec jako tlustou kružnici
    overlay = image.copy()
    cv2.circle(overlay, center, r2 + thickness // 2, (0, 0, 0), thickness=thickness)

    result = cv2.addWeighted(overlay, alpha_value, image, 1 - alpha_value, 0)

    return result

    """h, w = image.shape[:2]
    center = (w // 2, h // 2)
    outer_radius = int(np.hypot(w, h))  # přesahuje obraz

    # Maska s prstencem: 1.0 = plná aplikace alpha
    mask = np.zeros((h, w), dtype=np.float32)
    cv2.circle(mask, center, outer_radius, 1.0, -1)
    cv2.circle(mask, center, r, 0.0, -1)

    # Reshape masky pro RGB
    mask = mask.reshape(h, w, 1)

    # Převod na float32 pro výpočty
    image_f = image.astype(np.float32)
    black_overlay = np.zeros_like(image_f)

    # Alpha blending jen na místech masky
    result = image_f * (1 - mask * alpha_value) + black_overlay * (mask * alpha_value)
    result = np.clip(result, 0, 255).astype(np.uint8)
    return result"""

"""def add_transparent_ring(image):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    outer_radius = int(np.hypot(w, h))  # zajistí přetečení přes okraje

    # maska: 255 tam, kde bude prstenec
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, center, outer_radius, 255, -1)
    cv2.circle(mask, center, r, 0, -1)

    # overlay (černý) a příprava blendingu
    overlay = np.zeros_like(image, dtype=np.uint8)

    # PŘEVOD NA FLOAT PRO BLENDING
    image_f = image.astype(np.float32)
    mask_f = (mask / 255.0).reshape(h, w, 1).astype(np.float32)

    # blending
    result = image_f * (1 - mask_f * alpha_value)

    # ořízni hodnoty a zpět na uint8
    result = np.clip(result, 0, 255).astype(np.uint8)
    return result"""

"""
def add_transparent_ring(image):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    outer_radius = int(np.hypot(w, h))  # přetéká přes celý obrázek

    # maska: 255 tam, kde bude prstenec, 0 jinde (včetně díry)
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, center, outer_radius, 255, thickness=-1)
    cv2.circle(mask, center, r, 0, thickness=-1)

    # vytvoř černý overlay (stejný rozměr jako image)
    overlay = np.zeros_like(image, dtype=np.uint8)

    # převeď masku na float v rozsahu 0–1 a roztáhni na 3 kanály
    mask_float = (mask / 255.0).reshape(h, w, 1)  # shape (h, w, 1)
    
    # alpha blending
    blended = image * (1 - mask_float * alpha_value) + overlay * (mask_float * alpha_value)
    blended = blended.astype(np.uint8)

    return blended
"""