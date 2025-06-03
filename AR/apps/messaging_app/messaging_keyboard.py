from gui import keyboard



class MessagingKeyboard(keyboard.Keyboard):
    def __init__(self, layout: list[list[str]]):
        super().__init__(layout)

    def process_detected_key(self, detected_key):
        match detected_key:
            case "<-":
                if self.text and len(self.text) > self.cursor_in_text_position_from_back:
                    self.cursor_in_text_position_from_back += 1
            case "->":
                if self.text and self.cursor_in_text_position_from_back > 0:
                    self.cursor_in_text_position_from_back -= 1
            case "X":
                if self.text:
                    if len(self.text) > 0 and self.cursor_in_text_position_from_back < len(self.text):
                        cursor_position = len(self.text) - self.cursor_in_text_position_from_back
                        self.text = self.text[:cursor_position - 1] + self.text[
                                                                    cursor_position:]
            case _:
                self.text += detected_key