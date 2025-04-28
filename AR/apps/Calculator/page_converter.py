import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import numpy as np

from gui.elements.dropdown import Dropdown
from gui.elements.number_box import NumberBox
from gui.elements.button import Button
from apps.page_base import FixedAspectPage
from gui.color_manager import *
from gui.draw import is_cursor_in_rect
from other_utilities import Position, Size
from hand_detection_models import *

class Converter(FixedAspectPage):
    _file_path = Path(__file__).parent / "page_converter_data.json"  #  path to json file

    def __init__(self):
        self.quantities_data_list = []  # list of UnitData objects
        self.convert_json()  # Load the conversion data from JSON   
        self.quantities_options = [unit_data.name for unit_data in self.quantities_data_list] 
        self.current_units_options = []  # list of current unit options for the dropdown menus

        self.quantity_dropdown = Dropdown(Position(50, 50), Size(200, 40), self.quantities_options, None)
        self.unit_from_dropdown = Dropdown(Position(50, 100), Size(200, 40), [], None)
        self.unit_to_dropdown = Dropdown(Position(50, 150), Size(200, 40), [], None)
        self.numberbox_in = NumberBox(Position(50, 200), Size(200, 40))
        self.numberbox_out = NumberBox(Position(50, 250), Size(200, 40))
        self.btn_convert_num = Button(None, Position(50, 300), Size(200, 40), "Convert",
                                      get_nice_color(), get_neutral_color2(), get_font_color(),
                                      get_neutral_color(), get_nice_color(), get_font_color())
        
    def compute_aspect_ratio(self):
        pass
                                      

    def draw(self, overlay: np.ndarray, gestures: DetectionModel):
        w, h = self.size

        overlay = np.zeros((h, w, 4), dtype=np.uint8)

        self.convert_json()

        self.quantity_dropdown.draw(overlay, w, h, gestures)

        if(self.quantity_dropdown.selected_option is not None):
            selected_quantity = self.quantity_dropdown.options[self.quantity_dropdown.selected_option]

            for quantity in self.quantities_data_list:
                if quantity.name == selected_quantity:
                    self.current_units_options = [quantity.basic] + [name for name, _ in quantity.other]
                    self.unit_from_dropdown.options = self.current_units_options
                    self.unit_to_dropdown.options = self.current_units_options
        
        self.unit_from_dropdown.draw(overlay, w, h, gestures)
        self.unit_to_dropdown.draw(overlay, w, h, gestures)

        self.numberbox_in.draw(overlay, gestures)
        
        self.draw_btn(overlay, gestures)

        self.numberbox_out.draw(overlay, w, h, gestures)

        return overlay
    
    def draw_btn(self, image, left_click_gesture_detected, right_click_gesture_detected, left_cursor_position, right_cursor_position):
        is_left_hovered = is_cursor_in_rect(left_cursor_position, (self.btn_convert_num.x_pos, self.btn_convert_num.y_pos, self.btn_convert_num.x_pos + self.btn_convert_num._size[0], self.btn_convert_num.y_pos + self.btn_convert_num._size[1]))
        is_right_hovered = is_cursor_in_rect(right_cursor_position, (self.btn_convert_num.x_pos, self.btn_convert_num.y_pos, self.btn_convert_num.x_pos + self.btn_convert_num._size[0], self.btn_convert_num.y_pos + self.btn_convert_num._size[1]))
        is_left_clicked = is_left_hovered and left_click_gesture_detected
        is_right_clicked = is_right_hovered and right_click_gesture_detected
        is_clicked = is_left_clicked or is_right_clicked
        is_hovered = is_left_hovered or is_right_hovered

        if is_clicked:
            self.btn_click()

        self.btn_convert_num.draw(image, is_hovered)

    def btn_click(self):
        if self.quantities_data_list is not None:
            from_unit = self.unit_from_dropdown.options[self.unit_from_dropdown.selected_option]
            to_unit = self.unit_to_dropdown.options[self.unit_to_dropdown.selected_option]
            guantity = self.quantity_dropdown.options[self.quantity_dropdown.selected_option]
            in_number = self.numberbox_in.value
            out_number = self.ConvertNumber(in_number, guantity, from_unit, to_unit)
            
            self.numberbox_out.value = out_number

    def ConvertNumber(self, number: float, quantity: str, unit_from: str, unit_to: str) -> float:
        self.convert_json()  # Load the conversion data from JSON

        for unit_data in self.quantities_data_list:
            if unit_data.name == quantity:
                from_factor = None
                to_factor = None

                # base unit has factor 1
                if unit_from == unit_data.basic:
                    from_factor = 1
                if unit_to == unit_data.basic:
                    to_factor = 1

                for name, factor in unit_data.other:
                    if name == unit_from:
                        from_factor = factor
                    if name == unit_to:
                        to_factor = factor

                # Pokud jsme našli oba faktory, vypočti převod
                if from_factor is not None and to_factor is not None:
                    basic_value = number / from_factor  # převedeme na základní jednotku
                    converted_value = basic_value * to_factor  # z ní převedeme do cílové jednotky
                    return converted_value
                else:
                    print(f"Error: Unit '{unit_from}' or '{unit_to}' not found in '{quantity}'.")
                    return None

    def convert_json(self):
        if self._file_path.exists():
            try:
                with open(self._file_path, "r") as file:
                    json_data = json.load(file)
                    unit_data_list = [
                        UnitData.from_dict(name, data)
                        for name, data in json_data.items()
                    ]
                    self.quantities_data_list = unit_data_list
                    self.quantities_options = [unit_data.name for unit_data in unit_data_list]
                    #print("Loaded data:", unit_data_list)
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"Error loading calculator converter: {e}.")
                self.quantities_data_list = None
        else:
            print(f"File {self._file_path} does not exist.")
            self.quantities_data_list = None

@dataclass
class UnitData:
    name: str  # Name of the quantity (e.g., "length", "value")
    basic: str  # Basic unit (e.g., "m")
    other: List[Tuple[str, float]]  # List of other units with conversion factors

    @staticmethod
    def from_dict(name: str, data: dict) -> 'UnitData':
        return UnitData(
            name=name,
            basic=data["basic"],
            other=[(item[0], item[1]) for item in data["other"]]
        )