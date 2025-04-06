import os

class MenuItem:
    def __init__(self, name, display_name, iconPath):
        self._name = name
        self._display_name = display_name
        self._selected = False
        self._icon_path = iconPath

    def clicked(self):
        print(f"Položka '{self._name}' byla kliknuta.")

    def set_display_name(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name
    
    def get_name(self):
        return self._name
    
    def get_icon_path(self):
        base_path = os.path.dirname(__file__)  # Získá adresář aktuálního souboru
        return os.path.join(base_path, "..", "resources", "icons", self._icon_path)

class App(MenuItem):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.opened = False

    def clicked(self):
        super().clicked()
        if self.opened:
            self.close()
        else:
            self.launch()

    def launch(self):
        print(f"Spuštění aplikace {self._name}")
        #TODO: implementace spuštění aplikace
        self.opened = True

    def close(self):
        print(f"Zavření aplikace {self._name}")
        #TODO: implementace zavření aplikace
        self.opened = False

class LockMenu(MenuItem):
    def __init__(self, icons_path):
        super().__init__("MenuLock", "Pin Menu", icons_path[0])
        self.menu_pined = False
        self._icon_paths = icons_path

    def pin_menu(self):
        print(f"Menu '{self._name}' is pined")
        self._icon = self._icon_paths[0]
        self.menu_pined = True
        #TODO: implementace připnutí menu

    def unpin_menu(self):
        print(f"Menu '{self._name}' is unpined.")
        self._icon = self._icon_paths[1]
        self.menu_pined = False
        #TODO: implementace odepnutí menu

    def clicked(self):
        print(f"Menu '{self._name}' was clicked.")
        if self.menu_pined:
            self.unpin_menu()
        else:
            self.pin_menu()

class CloseMenu(MenuItem):
    def __init__(self, icon_path):
        super().__init__("CloseMenu", "Close Menu", icon_path)

    def clicked(self):
        super().clicked()
        self.close()

    def close(self):
        print(f"Menu '{self._name}' bylo zavřeno.")
        #TODO: implementace zavření menu"""
