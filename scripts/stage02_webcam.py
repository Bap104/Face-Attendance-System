"""Giai đoạn 2: chỉ mở webcam, chưa nhận diện."""

import cv2

from camera import open_camera, read_frame
from config import WINDOW_NAME
from utils.drawing import put_label


def main() -> None:
    cap = open_camera()
    print("Webcam đã mở. Nhấn Q để thoát.")
    try:
        while True:
            frame = read_frame(cap)
            if frame is None:
                print("Không đọc được frame.")
                break
            put_label(frame, "Stage 2: Webcam OK - nhan Q de thoat", (10, 36))
            cv2.imshow(WINDOW_NAME, frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
