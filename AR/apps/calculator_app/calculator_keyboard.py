import math

from gui.keyboard import Keyboard

MAX_LENGTH = 10

KEYS = [
    ["<-", "->", "^", "pi"],
    ["C", "()", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "X", "="]
]

class CalculatorKeyboard(Keyboard):
    def __init__(self):
        super().__init__(KEYS)
        self.evaluated = False
        self._text = "0"

    def process_detected_key(self, detected_key):
        if detected_key == "<-":
            if self._text and len(self._text) > self.cursor_in_text_position_from_back:
                self.cursor_in_text_position_from_back += 1
        elif detected_key == "->":
            if self._text and self.cursor_in_text_position_from_back > 0:
                self.cursor_in_text_position_from_back -= 1
        elif detected_key == "X":
            if self.evaluated:
                self._text = "0"
                self.evaluated = False
            if self._text:
                if len(self._text) > 0 and self.cursor_in_text_position_from_back < len(self._text):
                    cursor_position = len(self._text) - self.cursor_in_text_position_from_back
                    self._text = self._text[:cursor_position - 1] + self._text[cursor_position:] # deletes character on the place before cursor
                    #(cursor position from back stayes the same)
        elif detected_key == "C":
            self._text = "0"
            self.cursor_in_text_position_from_back = 0
        elif detected_key in "0123456789":
            if self.evaluated:
                self._text = ""
                self.cursor_in_text_position_from_back = 0
                self.evaluated = False
            if self._text == "0" or self._text == "":
                self._text = detected_key
            else:
                cursor_position = len(self._text) - self.cursor_in_text_position_from_back
                self._text = self._text[:cursor_position] + detected_key + self._text[cursor_position:]
        elif detected_key in "+-*/%^":
            cursor_position = len(self._text) - self.cursor_in_text_position_from_back
            # Add an operator if the last character is not an operator
            if self._text and self._text[cursor_position - 1] not in "+-*/%^":
                if self.evaluated:
                    self.cursor_in_text_position_from_back = 0
                    self.evaluated = False
                self._text = self._text[:cursor_position] + detected_key + self._text[cursor_position:]
        elif detected_key == "pi":
            cursor_position = len(self._text) - self.cursor_in_text_position_from_back
            if self.evaluated:
                self._text = ""
                self.cursor_in_text_position_from_back = 0
                self.evaluated = False
            self._text = self._text[:cursor_position] + detected_key + self._text[cursor_position:]
        elif detected_key == ".":
            cursor_position = len(self._text) - self.cursor_in_text_position_from_back

            # Přidání desetinné tečky pouze pokud:
            # 1. Před kurzorem je číslo (nebo text je prázdný a začínáme s "0.")
            # 2. V aktuálním čísle (od posledního operátoru nebo závorky) ještě není desetinná tečka
            if not self._text:
                self._text = "0."
            else:
                # Najdeme poslední operátor nebo závorku před kurzorem
                last_operator_pos = max(
                    self._text.rfind(op, 0, cursor_position) for op in "+-*/%()"
                )
                # Extrahujeme aktuální číslo
                current_number = self._text[last_operator_pos + 1:cursor_position]

                # Přidáme tečku, pokud aktuální číslo neobsahuje tečku
                if "." not in current_number:
                    self._text = self._text[:cursor_position] + "." + self._text[cursor_position:]
        elif detected_key == "()":
            cursor_position = len(self._text) - self.cursor_in_text_position_from_back

            # Add parentheses
            if not self._text or self._text[cursor_position-1] in "+-*/%(":
                self._text = self._text[:cursor_position] + "(" + self._text[cursor_position:]
            elif self._text[cursor_position - 1].isdigit() or self._text[cursor_position - 1] == ")":
                if self._text.count("(") > self._text.count(")"):
                    self._text = self._text[:cursor_position] + ")" + self._text[cursor_position:]
                else:
                    self._text = self._text[:cursor_position] + "(" + self._text[cursor_position:]
        elif detected_key == "=" and self._text:
            # Evaluate the expression
            try:
                self._text = self._text.replace("pi", str(math.pi))
                self._text = self._text.replace("^", "**")
                self._text = str(eval(self._text))
            except (SyntaxError, ZeroDivisionError):
                self._text = "Invalid"
            self.evaluated = True

        # Limit the text length
        self._text = self._text[:MAX_LENGTH]
        print(f"Current text: {self._text}")