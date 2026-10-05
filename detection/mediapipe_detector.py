"""Phát hiện khuôn mặt và landmark bằng MediaPipe.

MediaPipe Face Detection: tìm hộp khuôn mặt (nhanh, ổn định webcam).
MediaPipe Face Mesh: 468 điểm landmark (mắt, mũi, miệng) phục vụ alignment / liveness.
"""

from __future__ import annotations

import cv2
import mediapipe as mp
import numpy as np

from config import MEDIAPIPE_MIN_CONFIDENCE, MEDIAPIPE_MODEL_SELECTION


class MediaPipeFaceDetector:
    def __init__(self) -> None:
        self._mp_fd = mp.solutions.face_detection
        self._detector = self._mp_fd.FaceDetection(
            model_selection=MEDIAPIPE_MODEL_SELECTION,
            min_detection_confidence=MEDIAPIPE_MIN_CONFIDENCE,
        )

    def detect(self, frame_bgr: np.ndarray) -> list[tuple[int, int, int, int]]:
        h, w, _ = frame_bgr.shape
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        result = self._detector.process(rgb)
        boxes: list[tuple[int, int, int, int]] = []
        if not result.detections:
            return boxes
        for det in result.detections:
            bbox = det.location_data.relative_bounding_box
            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            bw = int(bbox.width * w)
            bh = int(bbox.height * h)
            x = max(0, x)
            y = max(0, y)
            boxes.append((x, y, bw, bh))
        return boxes

    def close(self) -> None:
        self._detector.close()


class MediaPipeFaceMesh:
    """468 landmark. Dùng cho alignment và (giai đoạn sau) chớp mắt."""

    def __init__(self, max_num_faces: int = 4) -> None:
        self._mp_mesh = mp.solutions.face_mesh
        self._mesh = self._mp_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def detect_landmarks(self, frame_bgr: np.ndarray) -> list[np.ndarray]:
        h, w, _ = frame_bgr.shape
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        result = self._mesh.process(rgb)
        faces: list[np.ndarray] = []
        if not result.multi_face_landmarks:
            return faces
        for face in result.multi_face_landmarks:
            pts = np.array(
                [(lm.x * w, lm.y * h) for lm in face.landmark],
                dtype=np.float32,
            )
            faces.append(pts)
        return faces

    def close(self) -> None:
        self._mesh.close()
