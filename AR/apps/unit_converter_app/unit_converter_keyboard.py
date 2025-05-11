from gui.keyboard import Keyboard

KEYS = [
            ["C", "X", "."],
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            ["0", "<-", "->"]
        ]

KEYES2 = [
            ["<-", "C", "X", ".", "->"],
            ["0", "1", "2", "3", "4"],
            ["5", "6", "7", "8", "9"]
        ]

MAX_LENGTH = 10

class ConverterKeyboard(Keyboard):
    def __init__(self):
        super().__init__(KEYS)
        self.equally_clicked = False
        self._text = ""

    def process_detected_key(self, detected_key):
        self.equally_clicked = False
        if detected_key == "X":
            if len(self._text) > 0 and self.cursor_in_text_position_from_back < len(self._text):
                cursor_position = len(self._text) - self.cursor_in_text_position_from_back
                self._text = self._text[:cursor_position - 1] + self._text[cursor_position:] # deletes character on the place before cursor
                #(cursor position from back stayes the same)
        elif detected_key == "C":
            self._text = "0"
            self.cursor_in_text_position_from_back = 0
        elif detected_key in "0123456789":
            # Přidání čísla
            if self._text == "0" or self._text == "":
                self._text = detected_key
            else:
                cursor_position = len(self._text) - self.cursor_in_text_position_from_back
                self._text = self._text[:cursor_position] + detected_key + self._text[cursor_position:]
        elif detected_key == ".":
            # Přidání čárky, pokud poslední znak je číslo a čárka již není v aktuálním čísle
            if self._text and self._text[-1].isdigit():
                # Zkontroluje, zda aktuální číslo již obsahuje čárku
                last_number = self._text.split()[-1]
                if "." not in last_number:
                    self._text += detected_key
            if not self._text:
                self._text = "0."
        elif detected_key == "=" and len(self._text) > 0:
            self.equally_clicked = True
        elif detected_key == "<-":
            if self._text and len(self._text) > self.cursor_in_text_position_from_back:
                self.cursor_in_text_position_from_back += 1
        elif detected_key == "->":
            if self._text and self.cursor_in_text_position_from_back > 0:
                self.cursor_in_text_position_from_back -= 1

        self._text = self._text[:MAX_LENGTH]