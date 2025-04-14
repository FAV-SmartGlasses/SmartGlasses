import math

import numpy as np

from Apps.calculator import Calculator
from Apps.settings import Settings
from gui.draw import *
from hand_detection import HandDetection
from menu_items import App, LockMenu, CloseMenu


class Menu:
    items = [
        App("Home", "Home", "Home.png"),
        #App("Settings", "Settings", "Settings.png"),
        Settings("Settings", "Settings", "Settings.png"),
        App("ToDo", "To DO", "Done.png"),
        #App("Calculator", "Calculator", "Plus.png"),
        Calculator("Calculator", "Calculator", "Plus.png"),
        #App("Browser", "Browser", "Search.png"),
        #App("Music", "Music", "Music.png"),
        App("Notes", "Notes", "Edit.png"),
        LockMenu(("Lock.png", "Padlock.png")),
        CloseMenu("Close.png")
    ]

    def __init__(self):
        self.items = Menu.items
        self._current_selection = 0
        self._visible = False

    def get_visible(self):
        return self._visible
    
    def set_visible(self, visible):
        self._visible = visible

    def display_menu(self, image, 
                     left_click_gesture_detected, right_click_gesture_detected, 
                     swipe_gesture_detected, 
                     left_cursor_position, right_cursor_position):
        h, w, _ = image.shape

        self.check_swipe_gesture(swipe_gesture_detected)
        
        if self._visible:
            self.detect_menu_item_selection(h, right_cursor_position)
            if self._current_selection is not None:
                self.check_click_gesture(right_click_gesture_detected)

            self._draw_menu(image, w, h)

        return image
    
    def check_swipe_gesture(self, swipe_gesture_detected):
        if swipe_gesture_detected == HandDetection.SwipeGesture.RIGHT and self._visible == False:
            self._visible = True
        elif swipe_gesture_detected == HandDetection.SwipeGesture.LEFT and self._visible == True:
            self._visible = False
    
    def detect_menu_item_selection(self, h, cursor_position):
        if cursor_position == (None, None):
            return
        
        padding = 15
        item_height = 50
        menu_height = padding + len(self.items) * (item_height + padding)
        menu_y = h // 2 - menu_height // 2

        for i, item in enumerate(self.items):
            item_y = menu_y + padding + i * (menu_height // len(self.items))

            middle_point_x, middle_point_y = cursor_position

            if item_y <= middle_point_y <= item_y + item_height:
                self._current_selection = i
                #print(f"Zelená čára ukazuje na: {self._items[i].get_name()}")
        
    def check_click_gesture(self, click_gesture_detected):
        if click_gesture_detected:
            self._visible = False
            self.items[self._current_selection].clicked()

    def _draw_menu(self, image, w, h):
        padding = 15
        item_height = 50
        menu_width = 2 * padding + item_height#300
        menu_height = padding + len(self.items) * (item_height + padding)
        menu_x = 10
        menu_y = h // 2 - menu_height // 2

        # Poloprůhledné pozadí menu
        overlay = image.copy()

        if True: #konstanta zda vykrelit pozadí pro menu
            draw_rounded_rectangle(overlay,
                                        (menu_x, menu_y), 
                                        (menu_x + menu_width, menu_y + menu_height), 
                                        30, 
                                        get_nice_color(), 
                                        -1)
            cv2.addWeighted(overlay, 0.4, image, 1 - 0.4, 0, image)

        # Zaoblené čtverce pro ikony
        for i, item in enumerate(self.items):
            if isinstance(item, App) and item.opened:
                color = get_nice_color()  # Barva pro otevřenou aplikaci
            else:
                color = get_neutral_color()  # Barva pro zavřenou aplikaci
            
            item_x = menu_x + padding
            item_y = menu_y + padding + i * (item_height + padding) #(menu_height // len(self._items))

            # Vyreslení bublin pro ikony
            radius = item_height // 2 if i != self._current_selection else math.ceil(item_height // 2 * 1.5)
            cv2.circle(image, 
                        (menu_x + (menu_width // 2 ), 
                            item_y + (item_height // 2 )), 
                        radius, 
                        color, 
                        -1)

            # Načtení a vykreslení ikony
            icon_path = item.get_icon_path()
            if icon_path:
                icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)
                if icon is not None:
                    icon_size = int(item_height / 5 * (3 if i != self._current_selection else 5))
                    icon = cv2.resize(icon, (icon_size, icon_size))  # Přizpůsobení velikosti ikony

                    padded_icon = np.zeros((item_height, item_height, 4), dtype=np.uint8)  # Vytvoření prázdného pozadí pro ikonu

                    # Výpočet pozice pro umístění ikony do středu
                    y_offset = (item_height - icon_size) // 2
                    x_offset = (item_height - icon_size) // 2

                    # Vložení ikony do středu matice
                    padded_icon[y_offset:y_offset + icon_size, x_offset:x_offset + icon_size] = icon

                    icon_y = item_y
                    icon_x = item_x
                    # Přidání ikony do menu
                    if icon.shape[2] == 4:  # Pokud má ikona alfa kanál
                        alpha_channel = icon[:, :, 3] / 255.0
                        for c in range(3):  # Pro RGB kanály
                            image[icon_y + y_offset:icon_y + y_offset + icon_size, icon_x + x_offset:icon_x + x_offset + icon_size, c] = (
                                alpha_channel * icon[:, :, c] +
                                (1 - alpha_channel) * image[icon_y + y_offset:icon_y + y_offset + icon_size, icon_x + x_offset:icon_x + x_offset + icon_size, c]
                            )
                    else:
                        image[icon_y + y_offset:icon_y + y_offset + icon_size, icon_x + x_offset:icon_x + x_offset + icon_size] = icon
            #cv2.putText(image, item.get_display_name(), (item_x + 20, item_y + item_height // 2 + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)