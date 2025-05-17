import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import List, Tuple, Union


class UnitConverterManager:
    _file_path = Path(__file__).parent / "unit_converter_data.json"  #  path to json file

    def __init__(self):
        self._quantities_data_list: tuple[UnitData]

    def get_quantities_options(self):
        self.convert_json()
        _quantities_options = [unit_data.name for unit_data in self._quantities_data_list]
        return _quantities_options
    
    def get_quantities_datalist(self):
        self.convert_json()
        return self._quantities_data_list
        
    def convert_json(self):
        if self._file_path.exists():
            try:
                with open(self._file_path, "r") as file:
                    json_data = json.load(file)
                    unit_data_list = [
                        UnitData.from_dict(name, data)
                        for name, data in json_data.items()
                    ]
                    #return unit_data_list
                    self._quantities_data_list = unit_data_list
                    #print("Loaded data:", unit_data_list)
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"Error loading calculator converter: {e}.")
                #return None
                self._quantities_data_list = None
        else:
            print(f"File {self._file_path} does not exist.")
            #return None
            self._quantities_data_list = None

    def convert_number(self, number: Union[int, float, str], quantity: str, unit_from: str, unit_to: str) -> float | None:
        self.convert_json()  # Load the conversion data from JSON

        try:
            number = Fraction(str(number))  # Přesný převod na zlomek
        except ValueError:
            print(f"Error: Cannot convert input '{number}' to a number.")
            return None

        for unit_data in self._quantities_data_list:
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
                    basic_value = number / Fraction(str(from_factor))
                    converted_value = basic_value * Fraction(str(to_factor))
                    return float(round(converted_value, 6))  # nebo vrátit přímo `converted_value` jako `Fraction` pokud nepotřebuješ float
                else:
                    print(f"Error: Unit '{unit_from}' or '{unit_to}' not found in '{quantity}'.")
                    return None


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
