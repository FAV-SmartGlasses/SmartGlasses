import cv2
import numpy as np
import time

class CameraManager:
    def __init__(self, scale_down: int = 4, show_fps = False, two_eyes = False):
        self.scale_down = scale_down  # Factor to resize the image
        self.show_fps = show_fps  # Flag to display FPS on the image
        self.two_eyes = two_eyes  # Flag to duplicate the image for two-eye display
        self.frame_count = 0  # Counter for frames processed
        self.prev_time = time.time()  # Time of the last FPS calculation
        self.cam_fps = None  # Calculated FPS value

    def process_frame(self, image):
        # Resize the image based on the scale_down factor
        original_h, original_w = image.shape[:2]
        resized_image = cv2.resize(image, (original_w - original_w // self.scale_down, original_h - original_h // self.scale_down))
        resized_h, resized_w = resized_image.shape[:2]

        # Calculate padding to center the resized image
        pad_top = (original_h - resized_h) // 2
        pad_bottom = original_h - resized_h - pad_top
        pad_left = (original_w - resized_w) // 2
        pad_right = (original_w - resized_w - pad_left)

        # Add padding to restore original width
        image = cv2.copyMakeBorder(resized_image, 0, 0, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        # Crop the image to focus on the central region
        target_width = image.shape[1] // 2
        image = image[:, target_width // 2:target_width // 2 + target_width]

        return image, resized_w, resized_h

    def make_two_eye_view(self, image, resized_w, resized_h):
        # Add padding to restore height and duplicate the image for two-eye view
        pad_top = (resized_h - resized_h // self.scale_down) // 2
        pad_bottom = resized_h - resized_h // self.scale_down - pad_top
        image = cv2.copyMakeBorder(image, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        image = np.hstack((image, image))
        return image

    def calculate_fps(self):
        # Calculate FPS based on the elapsed time and frame count
        self.frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - self.prev_time

        if elapsed_time > 1:
            self.cam_fps = self.frame_count / elapsed_time
            self.frame_count = 0
            self.prev_time = current_time

        return self.cam_fps

    def display_fps(self, image, resized_w, resized_h):
        # Display the calculated FPS on the image if enabled
        if self.show_fps and self.cam_fps is not None:
            text = "{:.2f}".format(self.cam_fps)
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
            text_x = (resized_w - text_size[0]) // 2
            text_y = (resized_h - text_size[1]) // 2
            cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
