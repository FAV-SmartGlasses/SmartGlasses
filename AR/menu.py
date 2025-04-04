import cv2
import math
from collections import deque

class Menu:
    items = ["Aplikace 1", "Aplikace 2", "Aplikace 3", "Aplikace 4", "Zavřít menu"]
    current_selection = 0
    visible = False
    #menu_position = 0  # Pozice pro pohyb nahoru/dolů v menu

    #def __init__(self):
        

    def draw_rounded_rectangle(image, top_left, bottom_right, radius, color, thickness):
        x1, y1 = top_left
        x2, y2 = bottom_right

        # Kreslíme 4 zaoblené rohy (kruhy) a 4 čáry
        cv2.circle(image, (x1 + radius, y1 + radius), radius, color, -1)
        cv2.circle(image, (x2 - radius, y1 + radius), radius, color, -1)
        cv2.circle(image, (x1 + radius, y2 - radius), radius, color, -1)
        cv2.circle(image, (x2 - radius, y2 - radius), radius, color, -1)
    
        cv2.rectangle(image, (x1 + radius, y1), (x2 - radius, y2), color, -1)
        cv2.rectangle(image, (x1, y1 + radius), (x2, y2 - radius), color, -1)

    def display_menu(image, current_selection, menu_visible, w, h):
        Menu.visible = menu_visible
        Menu.current_selection = current_selection
        if Menu.visible:
            menu_width = 300
            menu_height = 300
            padding = 20
            menu_x = 10
            menu_y = h // 2 - menu_height // 2

            # Poloprůhledné pozadí menu
            overlay = image.copy()
            cv2.rectangle(overlay, (menu_x, menu_y), (menu_x + menu_width, menu_y + menu_height), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.4, image, 1 - 0.4, 0, image)

            # Zaoblené čtverce pro ikony
            for i, item in enumerate(Menu.items):
                color = (0, 255, 255) if i == current_selection else (255, 255, 255)
                item_x = menu_x + padding
                item_y = menu_y + padding + i * (menu_height // len(Menu.items))

                # Kreslení zaoblených čtverců
                Menu.draw_rounded_rectangle(image, (item_x, item_y), (item_x + menu_width - 2 * padding, item_y + 40), 20, color, -1)
                cv2.putText(image, item, (item_x + 20, item_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        return image