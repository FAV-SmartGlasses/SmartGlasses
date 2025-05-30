from gui.keyboard import Keyboard

KEYS = [
            ['`', "1", "2", '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "(", ")"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "\\"],
            ["\\", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
            [" ", "->", "<-"]
        ]

class ToDoKeyboard(Keyboard):
    def __init__(self):
        super().__init__(KEYS)
    
    def process_detected_key(self, detected_key):
        if detected_key == "<-":
            if self._text and len(self._text) > self.cursor_in_text_position_from_back:
                self.cursor_in_text_position_from_back += 1
        elif detected_key == "->":
            if self._text and self.cursor_in_text_position_from_back > 0:
                self.cursor_in_text_position_from_back -= 1
        elif detected_key == "C":
            self._text = ""
            self.cursor_in_text_position_from_back = 0
        elif detected_key == "X":
             if len(self._text) > 0 and self.cursor_in_text_position_from_back < len(self._text):
                cursor_position = len(self._text) - self.cursor_in_text_position_from_back
                self._text = self._text[:cursor_position - 1] + self._text[cursor_position:] # deletes character on the place before cursor
        else:
            cursor_position = len(self._text) - self.cursor_in_text_position_from_back
            self._text = self._text[:cursor_position] + detected_key + self._text[cursor_position:]