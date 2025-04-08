import cv2

class Draw:
    def draw_rounded_rectangle(self, image, top_left, bottom_right, radius, color, thickness):
        x1, y1 = top_left
        x2, y2 = bottom_right

        # Kreslíme 4 zaoblené rohy (kruhy) a 4 čáry
        cv2.circle(image, (x1 + radius, y1 + radius), radius, color, -1)
        cv2.circle(image, (x2 - radius, y1 + radius), radius, color, -1)
        cv2.circle(image, (x1 + radius, y2 - radius), radius, color, -1)
        cv2.circle(image, (x2 - radius, y2 - radius), radius, color, -1)
    
        cv2.rectangle(image, (x1 + radius, y1), (x2 - radius, y2), color, -1)
        cv2.rectangle(image, (x1, y1 + radius), (x2, y2 - radius), color, -1)