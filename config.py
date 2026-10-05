"""Cấu hình chung của hệ thống điểm danh.

Các ngưỡng (threshold) KHÔNG phải số bất biến.
Hãy đo trên dữ liệu thật của lớp bạn rồi điều chỉnh.
"""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATASET_DIR = ROOT_DIR / "dataset" / "known_faces"
DATA_DIR = ROOT_DIR / "data"
MODELS_DIR = ROOT_DIR / "models"
ATTENDANCE_CSV = DATA_DIR / "attendance.csv"
STUDENTS_CSV = DATA_DIR / "students.csv"
EMBEDDINGS_PATH = DATA_DIR / "embeddings.npz"

CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Haar Cascade
HAAR_SCALE_FACTOR = 1.1
HAAR_MIN_NEIGHBORS = 5
HAAR_MIN_SIZE = (60, 60)

# MediaPipe Face Detection: 0 = gần camera (webcam), 1 = khuôn mặt nhỏ/xa
MEDIAPIPE_MODEL_SELECTION = 0
MEDIAPIPE_MIN_CONFIDENCE = 0.5

# Cosine similarity: càng gần 1 càng giống.
# InsightFace (ArcFace) thường dùng khoảng 0.35-0.45 (cosine distance)
# hoặc similarity ~ 0.4-0.6 tùy model. Cần tự đo.
RECOGNITION_THRESHOLD = 0.45

# Không điểm danh trùng trong N giây
ATTENDANCE_COOLDOWN_SECONDS = 8 * 60 * 60  # 1 buổi học ~ 8 giờ (cùng ngày)

WINDOW_NAME = "Face Attendance MVP"
