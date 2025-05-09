from gui.keyboard import Keyboard

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

MAX_LENGTH = 10

class ConverterKeyboard(Keyboard):
    def __init__(self):
        super().__init__(KEYS)
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