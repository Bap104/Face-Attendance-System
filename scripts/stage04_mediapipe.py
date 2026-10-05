"""Giai đoạn 4: MediaPipe Face Detection + Face Mesh landmark (chức năng gốc)."""

import cv2

from camera import open_camera, read_frame
from config import WINDOW_NAME
from detection.mediapipe_detector import MediaPipeFaceDetector, MediaPipeFaceMesh
from utils.drawing import draw_box, put_label


def main() -> None:
    cap = open_camera()
    detector = MediaPipeFaceDetector()
    mesh = MediaPipeFaceMesh(max_num_faces=4)
    print("MediaPipe. Nhấn D = chỉ box, M = mesh, Q = thoát.")
    show_mesh = True
    try:
        while True:
            frame = read_frame(cap)
            if frame is None:
                break
            boxes = detector.detect(frame)
            for box in boxes:
                draw_box(frame, box, color=(0, 200, 255))

            if show_mesh:
                for pts in mesh.detect_landmarks(frame):
                    for x, y in pts[::4]:
                        cv2.circle(frame, (int(x), int(y)), 1, (0, 255, 0), -1)

            mode = "box+mesh" if show_mesh else "box"
            put_label(frame, f"MediaPipe {mode} | faces={len(boxes)} | D/M/Q", (10, 36))
            cv2.imshow(WINDOW_NAME, frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ord("Q")):
                break
            if key in (ord("d"), ord("D")):
                show_mesh = False
            if key in (ord("m"), ord("M")):
                show_mesh = True
    finally:
        detector.close()
        mesh.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
