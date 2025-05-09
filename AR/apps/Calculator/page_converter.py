import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Union
import numpy as np
import cv2

from gui.elements.dropdown import Dropdown
from gui.elements.number_box import NumberBox
from gui.elements.button import Button
from apps.page_base import FixedAspectPage
from gui.color_manager import *
from gui.draw import *
from other_utilities import *
from hand_detection_models import *
from gui.keyboard import Keyboard


MAX_LENGTH = 10

KEYS = [
            [" ", "C", "X"],
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            [" ", "0", "."]
        ]

KEYES2 = [
            [" ", "C", "X", ".", ""],
            ["0", "1", "2", "3", "4"],
            ["5", "6", "7", "8", "9"]
        ]

class Converter(FixedAspectPage):
    _file_path = Path(__file__).parent / "page_converter_data.json"  #  path to json file

    def __init__(self):
        super().__init__()

        self.keyboard = ConverterKeyboard(KEYS)

        self.aspect_ratio = self.compute_aspect_ratio()

        self._size = Size(800, int(800 / self.aspect_ratio))
        self._position = Position(0, 0)

        self.quantities_data_list = []  # list of UnitData objects
        self.convert_json()  # Load the conversion data from JSON   
        self.quantities_options = [unit_data.name for unit_data in self.quantities_data_list] 
        self.current_units_options = []  # list of current unit options for the dropdown menus

        self.quantity_dropdown = Dropdown(Position(50, 50), Size(200, 40), self.quantities_options, None)
        self.unit_from_dropdown = Dropdown(Position(50, 200), Size(200, 40), [], None)
        self.unit_to_dropdown = Dropdown(Position(50, 400), Size(200, 40), [], None)
        self.numberbox_in = NumberBox(Position(200, 200), Size(200, 40))
        self.numberbox_out = NumberBox(Position(50, 250), Size(200, 40))

    def set_sizes(self):        
        # Výběr veličiny (Dropdownbox)
        quantity_selection_position_percent = Position(5, 5)
        quantity_selection_size_percent = Size(40, 10)

        # Výběr vstupní jednotky (Dropdownbox)
        input_unit_selection_position_percent = Position(5, 20)
        input_unit_selection_size_percent = Size(30, 10)

        # Vstupní číslo (Numberbox)
        input_number_position_percent = Position(5, 35)
        input_number_size_percent = Size(30, 15)

        # Výběr výstupní jednotky (Dropdownbox)
        output_unit_selection_position_percent = Position(5, 55)
        output_unit_selection_size_percent = Size(30, 10)

        # Výstupní číslo (Numberbox)
        output_number_position_percent = Position(5, 70)
        output_number_size_percent = Size(30, 15)

        # Keyboard
        keyboard_position_percent = Position(50, 5)
        keyboard_size_percent = Size(40, 90)

        self.quantity_dropdown.set_position_and_size(*set_size_and_position_by_ratio(self._position, self._size, quantity_selection_position_percent, quantity_selection_size_percent))
        self.unit_from_dropdown.set_position_and_size(*set_size_and_position_by_ratio(self._position, self._size, input_unit_selection_position_percent, input_unit_selection_size_percent))
        self.unit_to_dropdown.set_position_and_size(*set_size_and_position_by_ratio(self._position, self._size, output_unit_selection_position_percent, output_unit_selection_size_percent))
        self.numberbox_in.set_position_and_size(*set_size_and_position_by_ratio(self._position, self._size, input_number_position_percent, input_number_size_percent))
        self.numberbox_out.set_position_and_size(*set_size_and_position_by_ratio(self._position, self._size, output_number_position_percent, output_number_size_percent))

        (keyboard_position, keyboard_size) = set_size_and_position_by_ratio(self._position, self._size, keyboard_position_percent, keyboard_size_percent)
        
        key_padding_ratio_by_key_size = 0.2  # Ratio of padding to key size
        
        # Počet řádků a sloupců klávesnice
        num_rows = len(KEYS)
        num_cols = max(len(row) for row in KEYS)

        # Výpočet velikosti klávesy na základě šířky a výšky klávesnice
        scaled_key_size_w = keyboard_size.w / (num_cols + (num_cols - 1) * key_padding_ratio_by_key_size)
        scaled_key_size_h = keyboard_size.h / (num_rows + (num_rows - 1) * key_padding_ratio_by_key_size)
        scaled_key_size = int(min(scaled_key_size_w, scaled_key_size_h))  # Použijeme menší rozměr pro čtvercové klávesy

        # Výpočet paddingu na základě velikosti klávesy
        scaled_key_padding = int(scaled_key_size * key_padding_ratio_by_key_size)

        self.keyboard.set_position_and_size(keyboard_position, scaled_key_size, scaled_key_padding)

        """(keyboard_position, keyboard_size) = set_size_and_position_by_ratio(self._position, self._size, keyboard_position_percent, keyboard_size_percent)
        key_padding_ratio_by_key_size = 0.2  # Ratio of padding to key size
        scaled_key_size = int(keyboard_size.h / (len(KEYS[0]) * (1 + key_padding_ratio_by_key_size) - key_padding_ratio_by_key_size))  # Scale the key size
        scaled_key_padding = int(scaled_key_size * key_padding_ratio_by_key_size)  # Scale padding between keys

        self.keyboard.set_position_and_size(keyboard_position, scaled_key_size, scaled_key_padding)"""
        
    def compute_aspect_ratio(self):
        #TODO: compute_aspect_ratio in converter_page
        return 1

    def draw(self, overlay: np.ndarray, gestures: DetectionModel):
        cv2.setUseOptimized(True)

        # Dynamic scaling factor based on screen dimensions
        """scaled_key_size = int(KEY_SIZE * scale_factor)  # Scale the key size
        scaled_padding = int(PADDING * scale_factor)  # Scale padding between keys
        scaled_key_padding = int(scaled_padding // 2)"""

        """draw_rounded_rectangle(overlay,
                           (self._position.x, self._position.y),
                           (self._position.x + self._size.w, self._position.y + self._size.h),
                           30,
                           get_nice_color(),
                           -1)"""
        
        self.set_sizes()

        self.convert_json()

        self.quantity_dropdown.draw(overlay, gestures)

        if self.quantity_dropdown.selected_option_index is not None:
            selected_quantity = self.quantity_dropdown.options[self.quantity_dropdown.selected_option_index]

            for quantity in self.quantities_data_list:
                if quantity.name == selected_quantity:
                    self.current_units_options = [quantity.basic] + [name for name, _ in quantity.other]
                    self.unit_from_dropdown.options = self.current_units_options
                    self.unit_to_dropdown.options = self.current_units_options

        if (self.quantity_dropdown.selected_option_index is not None and 
            self.unit_from_dropdown.selected_option_index is not None and
            self.unit_to_dropdown.selected_option_index is not None):
            self.set_output_value()
        
        self.unit_from_dropdown.draw(overlay, gestures)
        self.unit_to_dropdown.draw(overlay, gestures)
        
        # Draw the keyboard with dynamically scaled keys
        self.keyboard.draw(overlay, 
                           #self._position.x + scaled_padding + 100, 
                           #self._position.y + 100, 
                           None, None,
                           gestures,
                           get_neutral_color_bgra(), get_neutral_color2_bgra(), get_font_color_bgra(), 
                           get_neutral_color2_bgra(), get_nice_color_bgra(), get_nice_color_bgra(), 
                           None, None,
                           #scaled_key_size,
                           #scaled_key_padding,
                           False)

        self.numberbox_in.value = self.keyboard.text
        self.numberbox_in.draw(overlay, gestures)
        self.numberbox_out.draw(overlay, gestures)

        return overlay

    def set_output_value(self):
        if self.quantities_data_list is not None:
            from_unit = self.unit_from_dropdown.options[self.unit_from_dropdown.selected_option_index]
            to_unit = self.unit_to_dropdown.options[self.unit_to_dropdown.selected_option_index]
            guantity = self.quantity_dropdown.options[self.quantity_dropdown.selected_option_index]
            in_number = self.numberbox_in.value
            out_number = self.ConvertNumber(in_number, guantity, from_unit, to_unit)
            
            self.numberbox_out.value = out_number

    def ConvertNumber(self, number: Union[int, float, str], quantity: str, unit_from: str, unit_to: str) -> float:
        self.convert_json()  # Load the conversion data from JSON

        try:
            number = float(number)  # Převod na float
        except ValueError:
            print(f"Error: Cannot convert input '{number}' to a number.")
            return None

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

class ConverterKeyboard(Keyboard):
    def __init__(self, layout: list[list[str]]):
        super().__init__(layout)
        self.equally_clicked = False
        self.text = ""

    def process_detected_key(self, detected_key):
        self.equally_clicked = False
        if detected_key == "X":
            # Smazání posledního znaku
            if self.text:
                self.text = self.text[:-1]
        if detected_key == "C":
            # Smazání celého textu
            self.text = ""
        elif detected_key in "0123456789":
            # Přidání čísla
            if self.text == "0":
                # Pokud text obsahuje pouze "0", nahradí se novým číslem
                self.text = detected_key
            else:
                self.text += detected_key
        elif detected_key == ".":
            # Přidání čárky, pokud poslední znak je číslo a čárka již není v aktuálním čísle
            if self.text and self.text[-1].isdigit():
                # Zkontroluje, zda aktuální číslo již obsahuje čárku
                last_number = self.text.split()[-1]
                if "." not in last_number:
                    self.text += detected_key
            if not self.text:
                self.text = "0."
        elif detected_key == "=" and len(self.text) > 0:
            self.equally_clicked = True

        self.text = self.text[:MAX_LENGTH]