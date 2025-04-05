import cv2
import math
import numpy as np
from collections import deque
import os

class MenuItem:
    def __init__(self, name, display_name, iconPath):
        self._name = name
        self._display_name = display_name
        self._selected = False
        self._icon_path = iconPath

    def select(self):
        print(f"Vybrána položka: {self.name}")
        self._selected = True

    def unselect(self):
        print(f"Zrušena volba položky: {self.name}")
        self.selected = False

    def clicked(self):
        print(f"Položka '{self.name}' byla kliknuta.")

    def set_display_name(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name
    
    def get_name(self):
        return self._name
    
    def get_icon_path(self):
        base_path = os.path.dirname(__file__)  # Získá adresář aktuálního souboru
        return os.path.join(base_path, "..", "resources", "icons", self._icon_path)
        return "resources\icons\{self._icon_path}"

class App(MenuItem):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.opened = False


    def launch(self):
        print(f"Spuštění aplikace {self._name}")
        #TODO: implementace spuštění aplikace
        self.opened = True


class LockMenu(MenuItem):
    def __init__(self, icons_path):
        super().__init__("MenuLock", "Pin Menu", icons_path[0])
        self.menu_pined = False
        self._icon_paths = icons_path

    def pin_menu(self):
        print(f"Menu '{self.name}' is pined")
        self._icon = self._icon_paths[0]
        self.menu_pined = True
        #TODO: implementace připnutí menu

    def unpin_menu(self):
        print(f"Menu '{self.name}' is unpined.")
        self._icon = self._icon_paths[1]
        self.menu_pined = False

    def clicked(self):
        print(f"Menu '{self.name}' was clicked.")
        if self.menu_pined:
            self.unpin_menu()
        else:
            self.pin_menu()


class CloseMenu(MenuItem):
    def __init__(self, icon_path):
        super().__init__("CloseMenu", "Close Menu", icon_path)

    def close(self):
        print(f"Menu '{self.name}' bylo zavřeno.")
        #TODO: implementace zavření menu"""

class Menu:
    #items = ["Home", "Settings", "Aplikace 3", "Aplikace 4", "Close menu"]
    #items_icon = ["Home.png", "Settings.png", "icon3.png", "icon4.png", "Cancel.png"]

    items = [
        App("Home", "Home", "Home.png"),
        App("Settings", "Settings", "Settings.png"),
        App("ToDo", "To DO", "Done.png"),
        #App("Calculator", "Calculator", "Plus.png"),
        #App("Browser", "Browser", "Search.png"),
        #App("Music", "Music", "Music.png"),
        App("Notes", "Notes", "Edit.png"),
        LockMenu(("Lock.png", "Padlock.png")),
        CloseMenu("Close.png")
    ]

    current_selection = 0
    visible = False

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

    def display_menu(self, image, current_selection, menu_visible, h):
        Menu.visible = menu_visible
        Menu.current_selection = current_selection
        if Menu.visible:
            padding = 15
            item_height = 50
            menu_width = 2 * padding + item_height#300
            menu_height = padding + len(Menu.items) * (item_height + padding)
            menu_x = 10
            menu_y = h // 2 - menu_height // 2

            # Poloprůhledné pozadí menu
            overlay = image.copy()

            if(True): #konstanta zda vykrelit pozadí pro menu
                Menu.draw_rounded_rectangle(overlay, 
                                            (menu_x, menu_y), 
                                            (menu_x + menu_width, menu_y + menu_height), 
                                            30, 
                                            (0, 0, 0), 
                                            -1)
                cv2.addWeighted(overlay, 0.4, image, 1 - 0.4, 0, image)

            # Zaoblené čtverce pro ikony
            for i, item in enumerate(Menu.items):
                #color = (0, 255, 255) if i == current_selection else (255, 255, 255)
                color = (255, 255, 255)
                item_x = menu_x + padding
                item_y = menu_y + padding + i * (item_height + padding) #(menu_height // len(Menu.items))

                # Kreslení zaoblených čtverců pro ikony
                """Menu.draw_rounded_rectangle(image, 
                                            (item_x, item_y), 
                                            (item_x + item_height, item_y + item_height), 
                                            20, 
                                            color, 
                                            -1)"""
                radius = item_height // 2 if i != current_selection else math.ceil(item_height // 2 * 1.5)
                cv2.circle(image, 
                            (menu_x + (menu_width // 2 ), 
                             item_y + (item_height // 2 )), 
                            radius, 
                            color, 
                            -1)
                #Menu.draw_rounded_rectangle(image, (item_x, item_y), (item_x + item_height, item_y + item_height), 20, color, -1)


                # Načtení a vykreslení ikony
                icon_path = item.get_icon_path()
                if icon_path:
                    icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)
                    if icon is not None:
                        icon_size = int(item_height / 5 * (3 if i != current_selection else 5))
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

        return image