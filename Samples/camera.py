import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.start()

while True:
    # Capture the frame
    frame = picam2.capture_array()

    # Convert to RGB (sRGB) if necessary
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the image in a window
    cv2.imshow("Webcam", frame_rgb)

    # Exit loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Stop the camera and close OpenCV windows
picam2.stop()
cv2.destroyAllWindows()