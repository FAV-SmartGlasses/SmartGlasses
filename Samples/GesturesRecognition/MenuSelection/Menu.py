import cv2
import mediapipe as mp
import math
from collections import deque

# Inicializace MediaPipe pro detekci ruky
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

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


# Nastavení menu a aplikací
#menu_items = ["Aplikace 1", "Aplikace 2", "Aplikace 3", "Aplikace 4", "Zavřít menu"]
menu_items = [
        App("Home", "Home", "Home.png"),
        App("Settings", "Settings", "Settings.png"),
        App("ToDo", "To DO", "Done.png"),
        App("Calculator", "Calculator", "Plus.png"),
        App("Browser", "Browser", "Search.png"),
        App("Music", "Music", "Music.png"),
        App("Notes", "Notes", "Edit.png"),
        LockMenu(("Lock.png", "Padlock.png")),
        CloseMenu("Close.png")
    ]
current_selection = 0
menu_visible = False
DIST_THRESHOLD = 40  # prahová hodnota pro "spojení prstů"

# Pomocné proměnné pro sledování gest
hand_state_history = deque(maxlen=20)
gesture_detected = False
menu_position = 0  # Pozice pro pohyb nahoru/dolů v menu

# Kamera
cap = cv2.VideoCapture(0)

# Pomocná proměnná pro sledování směru pohybu zápěstí
last_wrist_x = None

# Definice zaobleného menu
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

# Hlavní smyčka
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    h, w, _ = image.shape
    gesture_detected = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            def get_point(id):
                lm = hand_landmarks.landmark[id]
                return int(lm.x * w), int(lm.y * h)

            thumb_tip = get_point(mp_hands.HandLandmark.THUMB_TIP)
            index_tip = get_point(mp_hands.HandLandmark.INDEX_FINGER_TIP)

            # Vzdálenost mezi palcem a ukazováčkem
            distance = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])

            # Detekce "open" / "closed" stavu
            hand_state = 'closed' if distance < DIST_THRESHOLD else 'open'
            if not hand_state_history or hand_state != hand_state_history[-1]:
                hand_state_history.append(hand_state)

            # Sledování pohybu zápěstí pro otevření/zavření menu
            wrist = get_point(mp_hands.HandLandmark.WRIST)
            
            # Pokud jsme již zaznamenali poslední pozici zápěstí, zkontrolujeme pohyb
            if last_wrist_x is not None:
                # Pokud zápěstí se pohybuje zleva doprava (otevření menu)
                if wrist[0] > last_wrist_x + 50:  # Pohyb zprava
                    menu_visible = True

                # Pokud zápěstí se pohybuje zprava doleva (zavření menu)
                elif wrist[0] < last_wrist_x - 50:  # Pohyb zleva
                    menu_visible = False

            # Uložení poslední pozice zápěstí
            last_wrist_x = wrist[0]

            # Detekce pohybu ruky pro navigaci
            if menu_visible:
                menu_width = 300
                menu_height = 300
                padding = 20
                menu_x = 10
                menu_y = h // 2 - menu_height // 2
                for i, item in enumerate(menu_items):
                    item_x = menu_x + padding
                    item_y = menu_y + padding + i * (menu_height // len(menu_items))
                    item_height = 40  # výška tlačítka

                    middle_point_y = (thumb_tip[1] + index_tip[1]) // 2
                    if item_y <= middle_point_y <= item_y + item_height:
                        current_selection = i  # označ aktuálně vybrané tlačítko
                        # volitelně: zvýraznění nebo výpis
                        print(f"Zelená čára ukazuje na: {menu_items[i].getName()}")

                # Výběr nebo zavření
                if hand_state == 'closed':
                    if current_selection == len(menu_items) - 1:  # Poslední položka = zavření menu
                        menu_visible = False  # zavření menu
                    else:
                        print(f"Spuštěná aplikace: {menu_items[current_selection].getName()}")

            # Vytvoření bodu mezi palcem a ukazováčkem (polovina mezi těmito dvěma body)
            middle_point_x = (thumb_tip[0] + index_tip[0]) // 2
            middle_point_y = (thumb_tip[1] + index_tip[1]) // 2
            # Kreslení bodu mezi palcem a ukazováčkem (červený bod)
            cv2.circle(image, (middle_point_x, middle_point_y), 10, (0, 0, 255), -1)
            # Kreslení vodorovné čáry v místě bodu mezi palcem a ukazováčkem (zelená čára)
            cv2.line(image, (0, middle_point_y), (w, middle_point_y), (0, 255, 0), 2)  # Zelená čára

            # Kreslení ruky a pozic
            cv2.circle(image, thumb_tip, 10, (0, 0, 255), -1)
            cv2.circle(image, index_tip, 10, (0, 0, 255), -1)
            cv2.line(image, thumb_tip, index_tip, (255, 255, 0), 2)
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Zobrazení menu
    if menu_visible:
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
        for i, item in enumerate(menu_items):
            color = (0, 255, 255) if i == current_selection else (255, 255, 255)
            item_x = menu_x + padding
            item_y = menu_y + padding + i * (menu_height // len(menu_items))

            # Kreslení zaoblených čtverců
            draw_rounded_rectangle(image, (item_x, item_y), (item_x + menu_width - 2 * padding, item_y + 40), 20, color, -1)
            cv2.putText(image, item.getDisplayName(), (item_x + 20, item_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Zobrazení obrazu
    cv2.imshow('VR Menu', image)

    # Detekce stisknutí klávesy pro otevření/zavření menu
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC pro ukončení
        break
    if key == ord('m'):  # Stisknutím 'M' otevřeme/zavřeme menu
        menu_visible = not menu_visible

cap.release()
cv2.destroyAllWindows()