from dotenv import load_dotenv

from apps.app_base import FreeResizeApp
from gui import color_manager
from gui.draw import *
from gui.elements import dropdown, button
from hand_detection_models import DetectionModel
from other_utilities import *
from . import messaging_keyboard
from .communication import *

load_dotenv(os.path.abspath("../resources/.env"))

layout = [
    ['`', "1", "2", '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "(", ")"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "\\"],
    ["\\", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/"],
    ["->" ," ", "<-", "X"]
]

scaled_key_size = 0
scaled_padding = 0

class MessagingApp(FreeResizeApp):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.messaging_keyboard = messaging_keyboard.MessagingKeyboard(layout)
        self.messaging_keyboard.set_colors(color_manager.get_neutral_color_bgra(), color_manager.get_neutral_color2_bgra(), color_manager.get_font_color_bgra(),
                           color_manager.get_neutral_color2_bgra(), color_manager.get_nice_color_bgra(), color_manager.get_nice_color_bgra())

        self.initial_positions = [Position(x=25, y=150), Position(x=200, y=150), Position(90, 200)]

        self.server = dropdown.Dropdown(Position(x=100, y=100), Size(w=100, h=50), ["DMs", "OptiForge - SmartGlasses"])
        self.channel = dropdown.Dropdown(Position(x=50, y=50), Size(w=100, h=50), [])
        self.send = button.Button(None, Position(300, 400), Size(100, 25), "Send!",
                          get_neutral_color(), get_neutral_color(), get_font_color(),
                          get_nice_color(), get_neutral_color2(), get_font_color())

        self.messages = {}
        self.ai_messages = {}

        self.message_fetch = MessageFetch(self.messages, self.ai_messages)

        self.new_server = self.old_server = None

    def launch(self):
            #uncomment this when using discord messaging
        self.message_fetch.start()
        self.opened = True

    def close(self):
        self.message_fetch.stop()   #uncomment this when using discord messaging
        self.opened = False

    def update(self, send : bool):
        lock = threading.Lock()

        with lock:
            self.server.options = list(self.messages.keys())

        self.old_server = self.new_server
        self.new_server = self.server.selected_option_index

        if self.new_server != self.old_server:
            self.channel.selected_option_index = None

        if self.server.selected:
            self.channel.options = list(self.messages.get(self.server.selected_option).keys())
        else:
            self.channel.options = []

        if send and self.server.selected and self.channel.selected:
            send_message(self.messaging_keyboard._text, self.server.selected_option, self.channel.selected_option)

    def draw(self, image: np.ndarray, gestures: DetectionModel):
        """Draw the calculator UI dynamically based on the current size"""
        cv2.setUseOptimized(True)

        overlay = image.copy()

        if self.opened:
            self.check_fist_gesture(gestures)

            cols = len(layout[0])
            rows = len(layout)
            sample_key_size = 10  # libovolná jednotka, důležité jsou proporce
            sample_padding = sample_key_size // 2
            sample_key_padding = sample_padding // 2
            sample_textbox_height = sample_key_size

            total_width = cols * sample_key_size + (cols - 1) * sample_key_padding + 2 * sample_padding

            ratio = self._size.w / total_width

            scaled_padding = int(sample_padding * ratio)
            scaled_key_size = int(sample_key_size * ratio)
            scaled_key_padding = int(sample_key_padding * ratio)
            textbox_height = int(sample_textbox_height * ratio)

            # Draw the textbox background
            textbox_width = self._size.w
            draw_rounded_rectangle(
                overlay,
                self._position.get_array(),
                get_right_bottom_pos(self._position, self._size).get_array(),
                30,
                get_nice_color_bgra(),  # Use BGRA color
                -1)

            self.messaging_keyboard.set_position_and_size(
                Position(self._position.x + scaled_padding, self._position.y + textbox_height + scaled_padding),
                scaled_key_size,
                scaled_key_padding)

            self.server.set_position_and_size(
                Position(self._position.x + scaled_padding + self.initial_positions[0].x, self._position.y + textbox_height + scaled_padding + self.initial_positions[0].y), self.server._size
                )

            self.channel.set_position_and_size(
                Position(self._position.x + scaled_padding + self.initial_positions[1].x, self._position.y + textbox_height + scaled_padding + self.initial_positions[1].y),
                self.channel._size
            )

            self.send.set_position_and_size(
                Position(self._position.x + scaled_padding + self.initial_positions[2].x, self._position.y + textbox_height + scaled_padding + self.initial_positions[2].y),
                self.send._size
            )

            self.messaging_keyboard.draw(overlay, gestures)
            self.server.draw(overlay, gestures)
            self.channel.draw(overlay, gestures)
            self.send.draw(overlay, self.send.is_hovered_or_clicked(gestures)[0])

            # Kombinace původního obrázku a překryvného obrázku s průhledností
            alpha = get_app_transparency()
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

            # Draw the text inside the textbox
            text_size = cv2.getTextSize(self.messaging_keyboard._text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = self._position.x + (textbox_width - text_size[0]) // 2
            text_y = self._position.y + (textbox_height + text_size[1] + scaled_padding) // 2
            cv2.putText(
                image,
                self.messaging_keyboard.get_text_with_cursor(),
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                get_font_color_bgra(),  # Use BGRA color
                2)

            self.update(self.send.is_hovered_or_clicked(gestures)[1])

            if not self.server.selected or not self.channel.selected:
                return

            display_messages = list(self.messages.get(self.server.selected_option).get(self.channel.selected_option))

            for index, i in enumerate(display_messages[max(-5, -len(display_messages)-1):]):
                cv2.putText(image,
                            i.get("author") + ": " + i.get("content"),
                            (self._position.x + 0, index * 25 + 275 + self._position.y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            get_font_color_bgra(),
                            2
                            )

if __name__ == "__main__":
    send_message("Ahoj!", "3.E", "general")