from menu_items import MenuItem

class App(MenuItem):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.opened = False
        self.position = (0, 0)  # Pozice aplikace na obrazovce
        self.size = (300, 300) # Velikost aplikace
        self.pages = []  # Seznam stránek aplikace
        self.current_page = 0  # Index aktuální stránky

    def add_page(self, page):
        self.pages.append(page)

    def switch_page(self, page_index):
        if 0 <= page_index < len(self.pages):
            self.current_page = page_index
        else:
            print(f"Invalid page index: {page_index}")

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

    def draw(self, image, w, h, 
             left_click_gesture_detected, right_click_gesture_detected, 
             left_cursor_position, right_cursor_position):
        return image

