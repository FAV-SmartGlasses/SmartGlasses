from gui import keyboard



class MessagingKeyboard(keyboard.Keyboard):
    def __init__(self, layout: list[list[str]]):
        super().__init__(layout)

    def process_detected_key(self, detected_key):
        match detected_key:
            case "<-":
                if self._text and len(self._text) > self.cursor_in_text_position_from_back:
                    self.cursor_in_text_position_from_back += 1
            case "->":
                if self._text and self.cursor_in_text_position_from_back > 0:
                    self.cursor_in_text_position_from_back -= 1
            case "X":
                if self._text:
                    if len(self._text) > 0 and self.cursor_in_text_position_from_back < len(self._text):
                        cursor_position = len(self._text) - self.cursor_in_text_position_from_back
                        self._text = self._text[:cursor_position - 1] + self._text[
                                                                    cursor_position:]
            case _:
                self._text += detected_key