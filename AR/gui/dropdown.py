import cv2

class Dropdown:
    def __init__(self, x, y, width, height, options, base_color, option_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.base_color = base_color
        self.option_color = option_color
        self.active = False
        self.selected = options[0]

    @property
    def rect(self):
        return self.x, self.y, self.width, self.height

    @rect.setter
    def rect(self, value):
        self.x, self.y, self.width, self.height = value

    def draw(self, image):
        if self.active:
            overlay = image.copy()
            # Apply transparency (50%) to the dropdown
            for i, option in enumerate(self.options):
                option_y = self.y + self.height * (i + 1)
                cv2.rectangle(overlay, (self.x, int(option_y)), (self.x + self.width, int(option_y + self.height)),
                              self.option_color, -1)
            cv2.addWeighted(overlay, 0.5, image, 0.5, 0, image)  # 50% transparency for dropdown

            # Draw options with borders and text
            for i, option in enumerate(self.options):
                option_y = self.y + self.height * (i + 1)
                cv2.rectangle(image, (self.x, int(option_y)), (self.x + self.width, int(option_y + self.height)),
                              (0, 0, 0), 2)
                cv2.putText(image, option, (self.x + 10, int(option_y + self.height * 0.7)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    def handle_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Check if clicked within dropdown bounds
            if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
                self.active = not self.active  # Toggle the dropdown visibility

            # Handle option clicks when dropdown is active
            elif self.active:
                for i, option in enumerate(self.options):
                    option_y = self.y + self.height * (i + 1)
                    if option_y <= y <= option_y + self.height:
                        self.selected = option
                        self.active = False  # Close the dropdown after selection
                        break
                else:
                    # If clicked outside options, close the dropdown
                    self.active = False

    def get_selected(self):
        return self.selected