import time

import cv2

from camera_manager import CameraManager
from config import *
from gui.GUI_manager import GUImanager


def main():
    changed = True
    cv2.setUseOptimized(True)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
    
    recording = False
    recorded_frames = []
    filename = None

    ui_manager = GUImanager()
    camera_manager = CameraManager(scale_down=SCALE_DOWN, show_fps=SHOW_FPS, two_eyes=TWO_EYES)

    while True:
        success, image = cap.read()
        if not success:
            break

        image, resized_w, resized_h = camera_manager.process_frame(image)
        image = cv2.flip(image, 1)
        image = ui_manager.display_GUI(image)

        if TWO_EYES:
            image = camera_manager.make_two_eye_view(image, resized_w, resized_h)

        camera_manager.calculate_fps()
        camera_manager.display_fps(image, resized_w, resized_h)

        if recording:
            recorded_frames.append(image.copy())

        cv2.imshow('AR Menu', image)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("f") and changed:
            changed = False
            recording = not recording
            if recording:
                recorded_frames = []
                filename = f"{int(time.time())}.mp4"
                print(f"Started recording to memory")
            else:
                print(f"Stopped recording. Saving {len(recorded_frames)} frames to {filename}")
                if recorded_frames:
                    out = cv2.VideoWriter(
                        filename,
                        cv2.VideoWriter_fourcc(*'mp4v'),
                        int(camera_manager.cam_fps),
                        (recorded_frames[0].shape[1], recorded_frames[0].shape[0])
                    )
                    for frame in recorded_frames:
                        out.write(frame)
                    out.release()
                    print(f"Saved to {filename}")
                recorded_frames = []

        elif key != ord("f"):
            changed = True

        if key in [27, ord('q'), ord('Q')]:
            break
        if cv2.getWindowProperty('AR Menu', cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
