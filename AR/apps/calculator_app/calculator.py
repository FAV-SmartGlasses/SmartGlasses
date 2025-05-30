from apps.app_base import FixedAspectApp
from apps.calculator_app.calculator_keyboard import CalculatorKeyboard
from gui.draw import *
from hand_detection_models import *
from other_utilities import *


class Calculator(FixedAspectApp):
    def __init__(self, name: str, display_name: str, icon_path: str):
        super().__init__(name, display_name, icon_path)

        self.keyboard = CalculatorKeyboard()
        self.keyboard.set_colors(get_neutral_color_bgra(), get_neutral_color2_bgra(), get_font_color_bgra(), 
                                get_neutral_color2_bgra(), get_nice_color_bgra(), get_nice_color_bgra())

        self.aspect_ratio = self.compute_aspect_ratio()

        # Default size, will be dynamically updated
        self._size: Size = Size(300, int(300 / self.aspect_ratio))
        self._position: Position = Position(0, 0)

    def compute_aspect_ratio(self):
        """Compute the aspect ratio based on the layout"""
        cols = len(self.keyboard.keys[0])
        rows = len(self.keyboard.keys)
        sample_key_size = 10
        sample_padding = sample_key_size // 2
        sample_key_padding = sample_padding // 2
        sample_textbox_height = sample_key_size

        total_width = cols * sample_key_size + (cols - 1) * sample_key_padding + 2 * sample_padding
        total_height = rows * sample_key_size + (rows - 1) * sample_key_padding + sample_textbox_height + 2 * sample_padding

        return total_width / total_height

    def draw(self, image: np.ndarray, gestures: DetectionModel):
        cv2.setUseOptimized(True)

        overlay = image.copy()

        if self.opened:
            self.check_fist_gesture(gestures)
            self.draw_lines(image, gestures)
            #self.check_resize_gesture(gestures)

            cols = len(self.keyboard.keys[0])
            rows = len(self.keyboard.keys)
            sample_key_size = 10
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
            
            self.keyboard.set_position_and_size(
                                Position(self._position.x + scaled_padding, self._position.y + textbox_height + scaled_padding),
                                scaled_key_size,
                                scaled_key_padding)
            
            self.keyboard.draw(overlay, gestures)

            alpha = get_app_transparency()
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

            # Draw the text inside the textbox
            text_size = cv2.getTextSize(self.keyboard._text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = self._position.x + (textbox_width - text_size[0]) // 2
            text_y = self._position.y + (textbox_height + text_size[1] + scaled_padding) // 2
            cv2.putText(
                image,
                self.keyboard.get_text_with_cursor(),
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                get_font_color_bgra(),  # Use BGRA color
                2)