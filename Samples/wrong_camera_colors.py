import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.start()

while True:
    # Capture the frame
    frame = picam2.capture_array()

    # Display the image in a window
    cv2.imshow("Webcam", frame)

    # Exit loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

picam2.stop()
cv2.destroyAllWindows()