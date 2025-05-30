import os

class MenuItem:
    def __init__(self, name: str, display_name: str, icon_path: str):
        self._name = name
        self._display_name = display_name
        self._selected = False
        self._icon_path = icon_path

    def clicked(self):
        pass

    def set_display_name(self, display_name: str):
        self._display_name = display_name

    def get_display_name(self) -> str:
        return self._display_name

    def get_name(self) -> str:
        return self._name

    def get_icon_path(self) -> str:
        base_path = os.path.dirname(__file__)  # Získá adresář aktuálního souboru
        return os.path.join(base_path, "..", "resources", "icons", self._icon_path)

class CloseMenu(MenuItem):
    def __init__(self, icon_path: str):
        super().__init__("CloseMenu", "Close Menu", icon_path)

    def clicked(self):
        super().clicked()
        self.close()

    def close(self):
        pass