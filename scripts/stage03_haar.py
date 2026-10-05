"""Giai đoạn 3: phát hiện khuôn mặt bằng Haar Cascade (chức năng gốc)."""

import cv2

from camera import open_camera, read_frame
from config import WINDOW_NAME
from detection.haar_detector import HaarFaceDetector
from utils.drawing import draw_box, put_label


def main() -> None:
    cap = open_camera()
    detector = HaarFaceDetector()
    print("Haar Cascade. Nhìn vào camera. Nhấn Q để thoát.")
    try:
        while True:
            frame = read_frame(cap)
            if frame is None:
                break
            faces = detector.detect(frame)
            for box in faces:
                draw_box(frame, box, color=(0, 255, 0))
            put_label(frame, f"Haar faces: {len(faces)}  |  Q = quit", (10, 36))
            cv2.imshow(WINDOW_NAME, frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
