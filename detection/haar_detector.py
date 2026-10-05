"""Phát hiện khuôn mặt bằng Haar Cascade (OpenCV).

Haar Cascade KHÔNG nhận diện "ai đó là ai".
Nó chỉ trả lời: "Ở vị trí nào trên ảnh có khuôn mặt?"

Output: danh sách hộp (x, y, w, h) trên ảnh xám/màu.
"""

from __future__ import annotations

import cv2
import numpy as np

from config import HAAR_MIN_NEIGHBORS, HAAR_MIN_SIZE, HAAR_SCALE_FACTOR


class HaarFaceDetector:
    def __init__(self) -> None:
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.cascade = cv2.CascadeClassifier(cascade_path)
        if self.cascade.empty():
            raise FileNotFoundError(f"Không tải được Haar Cascade: {cascade_path}")

    def detect(self, frame_bgr: np.ndarray) -> list[tuple[int, int, int, int]]:
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=HAAR_SCALE_FACTOR,
            minNeighbors=HAAR_MIN_NEIGHBORS,
            minSize=HAAR_MIN_SIZE,
        )
        return [(int(x), int(y), int(w), int(h)) for x, y, w, h in faces]
