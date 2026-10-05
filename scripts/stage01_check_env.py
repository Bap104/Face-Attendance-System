"""Giai đoạn 1: kiểm tra môi trường Python, OpenCV, camera (không hiện cửa sổ lâu)."""

import platform
import sys


def main() -> None:
    print("Python:", sys.version)
    print("Machine:", platform.machine())
    print("Platform:", platform.platform())

    import cv2
    import numpy as np

    print("OpenCV:", cv2.__version__)
    print("NumPy:", np.__version__)
    print("Haar path:", cv2.data.haarcascades)

    try:
        import mediapipe as mp

        print("MediaPipe:", mp.__version__)
    except Exception as exc:
        print("MediaPipe CHƯA cài (cần cho giai đoạn 4):", exc)

    try:
        import insightface
        import onnxruntime as ort

        print("InsightFace:", insightface.__version__)
        print("ONNX Runtime:", ort.__version__)
        print("ONNX providers:", ort.get_available_providers())
    except Exception as exc:
        print("InsightFace/ONNX CHƯA cài (cần cho giai đoạn 6):", exc)

    from camera import open_camera, read_frame

    cap = open_camera()
    frame = read_frame(cap)
    cap.release()
    if frame is None:
        print("FAIL: mở được camera nhưng không đọc frame.")
        sys.exit(1)
    print("Camera OK, frame shape:", frame.shape)
    print("Giai đoạn 1 thành công.")


if __name__ == "__main__":
    main()
