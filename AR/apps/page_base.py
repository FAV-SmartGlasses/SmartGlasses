class Page:
    def Draw(self, w, h,
             left_click_gesture_detected, right_click_gesture_detected, 
             left_cursor_position, right_cursor_position):
        raise NotImplementedError("This method should be overridden in subclasses") 
    
class CalculatorPage(Page):
    def draw(self, w, h, 
             left_click_gesture_detected, right_click_gesture_detected, 
             left_cursor_position, right_cursor_position):
        raise NotImplementedError("This method should be overridden in subclasses") 
    
    def dynamic_draw(self, w, h, overlay,
             left_click_gesture_detected, right_click_gesture_detected, 
             left_cursor_position, right_cursor_position):
        raise NotImplementedError("This method should be overridden in subclasses")
