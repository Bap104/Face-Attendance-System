"""Mở webcam trên macOS (Apple Silicon).

OpenCV trên Mac nên dùng backend AVFoundation.
Nếu camera không mở được, thử CAMERA_INDEX = 1.
"""

from __future__ import annotations

import cv2

import platform

from config import CAMERA_INDEX, FRAME_HEIGHT, FRAME_WIDTH


def open_camera(index: int | None = None) -> cv2.VideoCapture:
    camera_index = CAMERA_INDEX if index is None else index
    sys_name = platform.system()

    if sys_name == "Darwin":
        cap = cv2.VideoCapture(camera_index, cv2.CAP_AVFOUNDATION)
    elif sys_name == "Windows":
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        # Fallback thử lại không chỉ định backend
        cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        raise RuntimeError(
            "Không mở được webcam.\n"
            "- Cấp quyền Camera: macOS (System Settings → Privacy & Security → Camera) / Windows (Settings → Privacy & Security → Camera).\n"
            "- Thử đổi CAMERA_INDEX trong config.py (0, 1, 2).\n"
            "- Đóng Zoom/Meet/FaceTime/Teams nếu đang chiếm camera."
        )

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    return cap


def read_frame(cap: cv2.VideoCapture):
    ok, frame = cap.read()
    if not ok or frame is None:
        return None
    frame = cv2.flip(frame, 1)
    return frame
