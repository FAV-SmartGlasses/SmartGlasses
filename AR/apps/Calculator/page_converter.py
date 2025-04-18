import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from apps.page_base import CalculatorPage


class Converter(CalculatorPage):
    _file_path = Path(__file__).parent / "page_converter_data.json"  # cesta k JSON souboru

    def draw(self, w, h,
             left_click_gesture_detected, right_click_gesture_detected, 
             left_cursor_position, right_cursor_position):
        image = w.new_image(640, 480, (255, 255, 255))

        return image

    def Convert(self):
        if self._file_path.exists():
            try:
                with open(self._file_path, "r") as file:
                    json_data = json.load(file)
                    unit_data_list = [
                        UnitData.from_dict(name, data)
                        for name, data in json_data.items()
                    ]
                    #print("Loaded data:", unit_data_list)
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"Error loading calculator converter: {e}.")
        else:
            print(f"File {self._file_path} does not exist.")

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