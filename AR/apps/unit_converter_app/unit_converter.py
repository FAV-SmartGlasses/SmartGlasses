from abc import ABC
from typing import List

from apps.app_base import FixedAspectApp
from apps.unit_converter_app.unit_converter_keyboard import *
from apps.unit_converter_app.unit_converter_manager import UnitConverterManager, UnitData
from gui.draw import *
from gui.elements.dropdown import Dropdown
from gui.elements.number_box import NumberBox
from hand_detection_models import *
from other_utilities import *


class UnitConverter(FixedAspectApp, ABC):
    def __init__(self, name: str, display_name: str, icon_path: str):
        super().__init__(name, display_name, icon_path)

        self.keyboard = ConverterKeyboard()
        self.keyboard.set_colors(get_neutral_color_bgra(), get_neutral_color2_bgra(), get_font_color_bgra(), 
                                get_neutral_color2_bgra(), get_nice_color_bgra(), get_nice_color_bgra())

        self._position = Position(0, 0)

        self.quantities_data_list: List[UnitData] = []  # list of UnitData objects
        self.manager = UnitConverterManager()
        self.quantities_data_list = self.manager.convert_json()  # Load the conversion data from JSON
        self.current_units_options = []  # list of current unit options for the dropdown menus

        self.quantity_dropdown = Dropdown(Position(50, 50), Size(200, 40), self.manager.get_quantities_options(), None)
        self.unit_from_dropdown = Dropdown(Position(50, 200), Size(200, 40), [], None)
        self.unit_to_dropdown = Dropdown(Position(50, 400), Size(200, 40), [], None)
        self.number_box_in = NumberBox(Position(200, 200), Size(200, 40))
        self.number_box_out = NumberBox(Position(50, 250), Size(200, 40))

    def set_sizes(self):
        quantity_selection_position_percent = Position(5, 5)
        quantity_selection_size_percent = Size(40, 10)

        input_unit_selection_position_percent = Position(5, 20)
        input_unit_selection_size_percent = Size(30, 10)

        input_number_position_percent = Position(5, 35)
        input_number_size_percent = Size(30, 15)

        output_unit_selection_position_percent = Position(5, 55)
        output_unit_selection_size_percent = Size(30, 10)

        output_number_position_percent = Position(5, 70)
        output_number_size_percent = Size(30, 15)

        # Keyboard
        keyboard_position_percent = Position(50, 5)
        keyboard_size_percent = Size(40, 90)

        self.quantity_dropdown.set_position_and_size(*set_size_and_position_by_ratio(self._position, self._size, quantity_selection_position_percent, quantity_selection_size_percent))
        self.unit_from_dropdown.set_position_and_size(*set_size_and_position_by_ratio(self._position, self._size, input_unit_selection_position_percent, input_unit_selection_size_percent))
        self.unit_to_dropdown.set_position_and_size(*set_size_and_position_by_ratio(self._position, self._size, output_unit_selection_position_percent, output_unit_selection_size_percent))
        self.number_box_in.set_position_and_size(*set_size_and_position_by_ratio(self._position, self._size, input_number_position_percent, input_number_size_percent))
        self.number_box_out.set_position_and_size(*set_size_and_position_by_ratio(self._position, self._size, output_number_position_percent, output_number_size_percent))

        (keyboard_position, keyboard_size) = set_size_and_position_by_ratio(self._position, self._size, keyboard_position_percent, keyboard_size_percent)
        
        key_padding_ratio_by_key_size = 0.2  # Ratio of padding to key size

        num_rows = len(KEYS)
        num_cols = max(len(row) for row in KEYS)

        scaled_key_size_w = keyboard_size.w / (num_cols + (num_cols - 1) * key_padding_ratio_by_key_size)
        scaled_key_size_h = keyboard_size.h / (num_rows + (num_rows - 1) * key_padding_ratio_by_key_size)
        scaled_key_size = int(min(scaled_key_size_w, scaled_key_size_h))

        scaled_key_padding = int(scaled_key_size * key_padding_ratio_by_key_size)

        self.keyboard.set_position_and_size(keyboard_position, scaled_key_size, scaled_key_padding)
        
    """def compute_aspect_ratio(self):
        #TODO: compute_aspect_ratio in converter_page
        return 1"""

    def draw(self, image: np.ndarray, gestures: DetectionModel):
        cv2.setUseOptimized(True)

        if gestures.right_hand.clicked:
            pass

        if self.opened:
            self.check_fist_gesture(gestures)
            self.draw_lines(image, gestures)

            overlay = image.copy()

            draw_rounded_rectangle(overlay,
                                    self._position.get_array(),
                                    get_right_bottom_pos(self._position, self._size).get_array(),
                                    30,
                                    get_nice_color(),
                                    -1)
            
            self.set_sizes()

            self.quantities_data_list = self.manager.get_quantities_datalist()

            if self.quantity_dropdown.selected:
                selected_quantity = self.quantity_dropdown.selected_option

                for quantity in self.quantities_data_list:
                    if quantity.name == selected_quantity:
                        self.current_units_options = [quantity.basic] + [name for name, _ in quantity.other]
                        self.unit_from_dropdown.options = self.current_units_options
                        self.unit_to_dropdown.options = self.current_units_options

            if (self.quantity_dropdown.selected and
                self.unit_from_dropdown.selected and
                self.unit_to_dropdown.selected):
                self.set_output_value()
            
            
            self.quantity_dropdown.draw(overlay, gestures)
            
            self.unit_from_dropdown.draw(overlay, gestures)
            self.unit_to_dropdown.draw(overlay, gestures)
            
            # Draw the keyboard with dynamically scaled keys
            self.keyboard.draw(overlay, gestures, False)

            self.number_box_in.value = self.keyboard.get_text_with_cursor()
            self.number_box_in.draw(overlay, gestures)
            self.number_box_out.draw(overlay, gestures)

            alpha = get_app_transparency()
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

    def set_output_value(self):
        if self.quantities_data_list is not None:
            from_unit = self.unit_from_dropdown.selected_option
            to_unit = self.unit_to_dropdown.selected_option
            quantity = self.quantity_dropdown.selected_option
            in_number = str(self.number_box_in.value).replace("|", "")  #self.keyboard.text
            out_number = self.manager.convert_number(in_number, quantity, from_unit, to_unit)
            
            self.number_box_out.value = out_number