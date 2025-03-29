import cv2
import numpy as np
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.start()

while True:
    frame = picam2.capture_array()

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

picam2.stop()
cv2.destroyAllWindows()