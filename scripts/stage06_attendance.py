"""Giai đoạn 6: Điểm danh tự động bằng nhận diện khuôn mặt realtime.

Quy trình:
  1. Mở camera (dùng open_camera hiện tại).
  2. Tự động load dữ liệu khuôn mặt đã đăng ký từ Stage 5.
  3. Nhận diện khuôn mặt realtime:
     - So sánh với TOÀN BỘ sinh viên trong database.
     - Kiểm tra ngưỡng nhận diện (threshold).
     - Nếu khớp đúng Identity:
         + Tự động điểm danh ghi nhận "CÓ MẶT" vào data/attendance.csv.
         + Mỗi người chỉ điểm danh 1 lần trong 1 ngày (không ghi trùng).
         + Hiển thị Họ tên, MSSV, trạng thái "CÓ MẶT" hoặc "ĐÃ ĐIỂM DANH HÔM NAY".
     - Nếu KHÔNG khớp (khoảng cách > threshold / người lạ):
         + Hiển thị "UNKNOWN - Chưa đăng ký" (box màu đỏ).
         + Tuyệt đối KHÔNG điểm danh và KHÔNG lấy tên của người khác.
  4. Nhấn Q để thoát.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

# Đảm bảo nhận diện được thư mục gốc khi chạy trực tiếp
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cv2

from attendance.csv_store import auto_mark_attendance, get_attendance_store
from camera import open_camera, read_frame
from config import WINDOW_NAME
from detection.mediapipe_detector import MediaPipeFaceDetector
from recognition.face_manager import get_face_manager
from utils.drawing import draw_box, put_label


def main() -> None:
    print("=" * 60)
    print("      STAGE 6: ĐIỂM DANH BẰNG NHẬN DIỆN KHUÔN MẶT REALTIME")
    print("=" * 60)

    # 1. Tự động nạp dữ liệu sinh viên và mô hình nhận diện
    face_manager = get_face_manager()
    face_manager.load_data()
    store = get_attendance_store()

    print(f"\n[DỮ LIỆU ĐÃ ĐĂNG KÝ] Tổng số sinh viên: {len(face_manager.students)}")
    if len(face_manager.students) == 0:
        print("  -> CHÚ Ý: Chưa có khuôn mặt nào được đăng ký!")
        print("  -> Vui lòng chạy Stage 5 để đăng ký khuôn mặt trước.\n")
    else:
        for sid, sname in face_manager.students.items():
            print(f"  - {sid}: {sname}")
        print()

    # 2. Mở camera
    cap = open_camera()
    detector = MediaPipeFaceDetector()

    print("Camera đã mở. Hệ thống đang nhận diện realtime...")
    print("Nhấn phím 'Q' để thoát.\n")

    fh, fw = 720, 1280
    try:
        while True:
            frame = read_frame(cap)
            if frame is None:
                break
            fh, fw = frame.shape[:2]

            boxes = detector.detect(frame)

            for box in boxes:
                x, y, w, h = box

                # Crop khuôn mặt để nhận diện
                pad_w = int(w * 0.08)
                pad_h = int(h * 0.08)
                x1 = max(0, x - pad_w)
                y1 = max(0, y - pad_h)
                x2 = min(fw, x + w + pad_w)
                y2 = min(fh, y + h + pad_h)
                face_crop = frame[y1:y2, x1:x2]

                if face_crop.size == 0:
                    continue

                # Nhận diện: so sánh với toàn bộ database và kiểm tra threshold nghiêm ngặt
                sid, name, score = face_manager.recognize(face_crop)

                # Trường hợp 1: Nhận diện thành công người đã đăng ký
                if sid != "Unknown":
                    already_marked = store.already_marked_today(sid)

                    # Tự động điểm danh (nếu hôm nay chưa điểm danh)
                    record = auto_mark_attendance(student_id=sid, name=name, status="PRESENT")
                    if record is not None:
                        print(
                            f"✓ [ĐIỂM DANH MỚI] {record['name']} | MSSV: {record['student_id']} | "
                            f"Ngày: {record['date']} | Giờ: {record['time']} | Trạng thái: Có mặt"
                        )

                    # Hiển thị thông tin màu xanh lá
                    draw_box(frame, box, color=(0, 255, 0), thickness=2)
                    put_label(frame, f"{name} ({sid})", (x, max(24, y - 8)), color=(0, 255, 0))

                    if already_marked and record is None:
                        status_str = "DA DIEM DANH HOM NAY"
                    else:
                        status_str = f"CO MAT - {datetime.now().strftime('%H:%M:%S')}"

                    put_label(frame, status_str, (x, y + h + 24), color=(0, 255, 0))

                # Trường hợp 2: Người lạ / Chưa đăng ký / Không đạt ngưỡng threshold
                else:
                    # Tuyệt đối không điểm danh, không lấy tên người khác
                    draw_box(frame, box, color=(0, 0, 255), thickness=2)
                    put_label(frame, "UNKNOWN", (x, max(24, y - 8)), color=(0, 0, 255))
                    put_label(frame, "Chua dang ky", (x, y + h + 24), color=(0, 0, 255))

            # Thanh thông tin ở góc trên
            info_bar = (
                f"Stage 6: Diem danh | Da dang ky: {len(face_manager.students)} | Q = Thoat"
            )
            put_label(frame, info_bar, (10, 36), color=(255, 200, 0))

            cv2.imshow(WINDOW_NAME, frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
                break

    finally:
        detector.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
