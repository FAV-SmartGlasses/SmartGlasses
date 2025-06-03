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
        self.text = "0"

    def process_detected_key(self, detected_key):
        if detected_key == "<-":
            if self.text and len(self.text) > self.cursor_in_text_position_from_back:
                self.cursor_in_text_position_from_back += 1
        elif detected_key == "->":
            if self.text and self.cursor_in_text_position_from_back > 0:
                self.cursor_in_text_position_from_back -= 1
        elif detected_key == "X":
            if self.evaluated:
                self.text = "0"
                self.evaluated = False
            if self.text:
                if len(self.text) > 0 and self.cursor_in_text_position_from_back < len(self.text):
                    cursor_position = len(self.text) - self.cursor_in_text_position_from_back
                    self.text = self.text[:cursor_position - 1] + self.text[cursor_position:] # deletes character on the place before cursor
        elif detected_key == "C":
            self.text = "0"
            self.cursor_in_text_position_from_back = 0
        elif detected_key in "0123456789":
            if self.evaluated:
                self.text = ""
                self.cursor_in_text_position_from_back = 0
                self.evaluated = False
            if self.text == "0" or self.text == "":
                self.text = detected_key
            else:
                cursor_position = len(self.text) - self.cursor_in_text_position_from_back
                self.text = self.text[:cursor_position] + detected_key + self.text[cursor_position:]
        elif detected_key in "+-*/%^":
            cursor_position = len(self.text) - self.cursor_in_text_position_from_back
            # Add an operator if the last character is not an operator
            if self.text and self.text[cursor_position - 1] not in "+-*/%^":
                if self.evaluated:
                    self.cursor_in_text_position_from_back = 0
                    self.evaluated = False
                self.text = self.text[:cursor_position] + detected_key + self.text[cursor_position:]
        elif detected_key == "pi":
            cursor_position = len(self.text) - self.cursor_in_text_position_from_back
            if self.evaluated:
                self.text = ""
                self.cursor_in_text_position_from_back = 0
                self.evaluated = False
            self.text = self.text[:cursor_position] + detected_key + self.text[cursor_position:]
        elif detected_key == ".":
            cursor_position = len(self.text) - self.cursor_in_text_position_from_back

            if not self.text:
                self.text = "0."
            else:
                last_operator_pos = max(
                    self.text.rfind(op, 0, cursor_position) for op in "+-*/%()"
                )

                current_number = self.text[last_operator_pos + 1:cursor_position]

                if "." not in current_number:
                    self.text = self.text[:cursor_position] + "." + self.text[cursor_position:]
        elif detected_key == "()":
            cursor_position = len(self.text) - self.cursor_in_text_position_from_back

            if not self.text or self.text[cursor_position - 1] in "+-*/%(":
                self.text = self.text[:cursor_position] + "(" + self.text[cursor_position:]
            elif self.text[cursor_position - 1].isdigit() or self.text[cursor_position - 1] == ")":
                if self.text.count("(") > self.text.count(")"):
                    self.text = self.text[:cursor_position] + ")" + self.text[cursor_position:]
                else:
                    self.text = self.text[:cursor_position] + "(" + self.text[cursor_position:]
        elif detected_key == "=" and self.text:
            # Evaluate the expression
            try:
                self.text = self.text.replace("pi", str(math.pi))
                self.text = self.text.replace("^", "**")
                self.text = str(eval(self.text))
            except (SyntaxError, ZeroDivisionError):
                self.text = "Invalid"
            self.evaluated = True

        # Limit the text length
        self.text = self.text[:MAX_LENGTH]
        print(f"Current text: {self.text}")