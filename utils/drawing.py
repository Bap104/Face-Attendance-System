"""Vẽ khung và chữ lên frame OpenCV (BGR)."""

import cv2
import numpy as np


def draw_box(frame: np.ndarray, box, color=(0, 255, 0), thickness=2):
    x, y, w, h = [int(v) for v in box]
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)


def put_label(frame: np.ndarray, text: str, origin, color=(0, 255, 0)):
    x, y = int(origin[0]), int(origin[1])
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.6
    thickness = 2
    (tw, th), baseline = cv2.getTextSize(text, font, scale, thickness)
    cv2.rectangle(frame, (x, y - th - 8), (x + tw + 4, y + baseline), color, -1)
    cv2.putText(frame, text, (x + 2, y - 4), font, scale, (0, 0, 0), thickness, cv2.LINE_AA)
