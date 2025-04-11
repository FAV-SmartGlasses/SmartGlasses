import cv2


def draw_rounded_rectangle(image, top_left, bottom_right, radius, color, thickness):
    x1, y1 = top_left
    x2, y2 = bottom_right

    if(thickness == -1):
        # Kreslíme 4 zaoblené rohy (kruhy) a 4 čáry
        cv2.circle(image, (x1 + radius, y1 + radius), radius, color, -1)
        cv2.circle(image, (x2 - radius, y1 + radius), radius, color, -1)
        cv2.circle(image, (x1 + radius, y2 - radius), radius, color, -1)
        cv2.circle(image, (x2 - radius, y2 - radius), radius, color, -1)

        cv2.rectangle(image, (x1 + radius, y1), (x2 - radius, y2), color, -1)
        cv2.rectangle(image, (x1, y1 + radius), (x2, y2 - radius), color, -1)
    else:
        # Kreslení čtyř čtvrtkružnic
        cv2.ellipse(image, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)  # Levý horní roh
        cv2.ellipse(image, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)  # Pravý horní roh
        cv2.ellipse(image, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)   # Levý dolní roh
        cv2.ellipse(image, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)    # Pravý dolní roh

        # Kreslení čtyř přímek
        cv2.line(image, (x1 + radius, y1), (x2 - radius, y1), color, thickness)  # Horní strana
        cv2.line(image, (x1 + radius, y2), (x2 - radius, y2), color, thickness)  # Dolní strana
        cv2.line(image, (x1, y1 + radius), (x1, y2 - radius), color, thickness)  # Levá strana
        cv2.line(image, (x2, y1 + radius), (x2, y2 - radius), color, thickness)  # Pravá strana