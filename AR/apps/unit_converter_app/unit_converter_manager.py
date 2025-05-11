import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Union
import numpy as np
import cv2

class UnitConverterManager:
    _file_path = Path(__file__).parent / "unit_converter_data.json"  #  path to json file

    def __init__(self):
        pass
        
    def convert_json(self):
        if self._file_path.exists():
            try:
                with open(self._file_path, "r") as file:
                    json_data = json.load(file)
                    unit_data_list = [
                        UnitData.from_dict(name, data)
                        for name, data in json_data.items()
                    ]
                    return unit_data_list
                    #self.quantities_data_list = unit_data_list
                    #self.quantities_options = [unit_data.name for unit_data in unit_data_list]
                    #print("Loaded data:", unit_data_list)
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"Error loading calculator converter: {e}.")
                return None
                #self.quantities_data_list = None
        else:
            print(f"File {self._file_path} does not exist.")
            return None
            #self.quantities_data_list = None

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
