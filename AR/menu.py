import cv2
import math
from collections import deque

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

    def setDisplayName(self, display_name):
        self._display_name = display_name

    def getDisplayName(self):
        return self._display_name
    
    def getName(self):
        return self._name
    
    def getIconPath(self):
        return self.icon_path

class App(MenuItem):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.opened = False


    def launch(self):
        print(f"Spuštění aplikace {self.app_name}")
        #TODO: implementace spuštění aplikace
        self.opened = True


class LockMenu(MenuItem):
    def __init__(self, icons_path):
        super().__init__("MenuLock", "Pin Menu", icons_path[0])
        self.menu_pined = False
        self._iconPaths = icons_path

    def pin_menu(self):
        print(f"Menu '{self.name}' is pined")
        self._icon = self._iconPaths[0]
        self.menu_pined = True
        #TODO: implementace připnutí menu

    def unpin_menu(self):
        print(f"Menu '{self.name}' is unpined.")
        self._icon = self._iconPaths[1]
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

    def display_menu(self, image, current_selection, menu_visible, h):
        Menu.visible = menu_visible
        Menu.current_selection = current_selection
        if Menu.visible:
            padding = 20
            item_height = 50
            menu_width = 300
            menu_height = len(Menu.items) * (item_height + padding)
            menu_x = 10
            menu_y = h // 2 - menu_height // 2

            # Poloprůhledné pozadí menu
            overlay = image.copy()
            cv2.rectangle(overlay, (menu_x, menu_y), (menu_x + menu_width + padding, menu_y + menu_height + padding), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.4, image, 1 - 0.4, 0, image)

            # Zaoblené čtverce pro ikony
            for i, item in enumerate(Menu.items):
                color = (0, 255, 255) if i == current_selection else (255, 255, 255)
                item_x = menu_x + padding
                item_y = menu_y + padding + i * (item_height + padding) #(menu_height // len(Menu.items))

                # Kreslení zaoblených čtverců
                Menu.draw_rounded_rectangle(image, (item_x, item_y), (item_x + menu_width - 2 * padding, item_y + item_height), 20, color, -1)
                cv2.putText(image, item.getDisplayName(), (item_x + 20, item_y + item_height // 2 + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        return image