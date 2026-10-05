"""Giai đoạn 5: Đăng ký khuôn mặt mới và lưu dữ liệu persistent.

Quy trình:
  1. Nhập Họ và tên, MSSV/ID.
  2. Mở camera (dùng hàm open_camera hiện tại).
  3. Phát hiện khuôn mặt và thu thập chùm ảnh mẫu.
  4. Lưu persistent vào:
     - data/students.csv
     - data/face_model.yml
     - dataset/known_faces/{student_id}/
  5. Đóng chương trình và mở lại KHÔNG cần đăng ký lại.
"""

from __future__ import annotations

from pathlib import Path
import sys
import time

# Đảm bảo nhận diện được thư mục gốc khi chạy trực tiếp
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cv2

from camera import open_camera, read_frame
from config import WINDOW_NAME
from detection.mediapipe_detector import MediaPipeFaceDetector
from recognition.face_manager import get_face_manager
from utils.drawing import draw_box, put_label


def register_face(student_id: str, name: str) -> bool:
    """Mở camera và chụp chùm ảnh khuôn mặt để lưu persistent."""
    cap = open_camera()
    detector = MediaPipeFaceDetector()
    face_manager = get_face_manager()

    print("\n[CAMERA ĐÃ MỞ]")
    print(f"  -> Đăng ký cho: {name} (MSSV: {student_id})")
    print("  -> Hãy nhìn thẳng vào camera.")
    print("  -> Nhấn phím SPACE (phím cách) hoặc phím 'S' để CHỤP & LƯU.")
    print("  -> Nhấn phím 'Q' để HỦY.\n")

    registered = False
    try:
        while True:
            frame = read_frame(cap)
            if frame is None:
                print("Không đọc được frame từ camera.")
                break

            boxes = detector.detect(frame)
            has_face = len(boxes) > 0

            if has_face:
                box = boxes[0]
                draw_box(frame, box, color=(0, 255, 0), thickness=2)
                put_label(
                    frame,
                    f"Dang ky: {name} - {student_id}",
                    (10, 36),
                    color=(0, 255, 0),
                )
                put_label(
                    frame,
                    "Nhan SPACE hoac S de CHUP & LUU | Q de huy",
                    (10, 70),
                    color=(255, 200, 0),
                )
            else:
                put_label(
                    frame,
                    "Vui long huong mat ve phia camera...",
                    (10, 36),
                    color=(0, 0, 255),
                )
                put_label(
                    frame,
                    f"Dang ky: {name} - {student_id} | Q = Huy",
                    (10, 70),
                    color=(200, 200, 200),
                )

            cv2.imshow(WINDOW_NAME, frame)
            key = cv2.waitKey(1) & 0xFF

            if key in (ord("q"), ord("Q")):
                print("[HỦY BỎ] Người dùng hủy quá trình đăng ký.")
                break

            # Phím SPACE (32) hoặc 's' / 'S' để bắt đầu chụp
            if key in (32, ord("s"), ord("S")):
                if not has_face:
                    print("Chưa phát hiện khuôn mặt rõ ràng, vui lòng nhìn vào camera!")
                    continue

                print("\nĐang thu thập mẫu khuôn mặt...")
                collected_faces: list = []
                fh, fw = frame.shape[:2]

                # Chụp chùm 15 frame liên tiếp để thu thập đa dạng góc nhìn
                for i in range(15):
                    f = read_frame(cap)
                    if f is None:
                        continue
                    bxs = detector.detect(f)
                    if len(bxs) > 0:
                        bx, by, bw, bh = bxs[0]
                        # Thêm margin 10% quanh khuôn mặt
                        pad_w = int(bw * 0.1)
                        pad_h = int(bh * 0.1)
                        x1 = max(0, bx - pad_w)
                        y1 = max(0, by - pad_h)
                        x2 = min(fw, bx + bw + pad_w)
                        y2 = min(fh, by + bh + pad_h)
                        face_crop = f[y1:y2, x1:x2]
                        if face_crop.size > 0:
                            collected_faces.append(face_crop)
                            draw_box(f, bxs[0], color=(0, 255, 255), thickness=2)
                            put_label(
                                f,
                                f"Dang thu thap mau: {len(collected_faces)}/15",
                                (10, 36),
                                color=(0, 255, 255),
                            )
                            cv2.imshow(WINDOW_NAME, f)
                            cv2.waitKey(50)

                if len(collected_faces) < 5:
                    print("[LỖI] Không thu thập đủ mẫu ảnh rõ nét. Vui lòng thử lại!")
                    continue

                # Lưu dữ liệu persistent
                face_manager.save_student(
                    student_id=student_id,
                    name=name,
                    face_images=collected_faces,
                )

                # Hiển thị thông báo thành công
                put_label(
                    frame,
                    "DANG KY THANH CONG! DA LUU DU LIEU.",
                    (10, 110),
                    color=(0, 255, 0),
                )
                cv2.imshow(WINDOW_NAME, frame)
                cv2.waitKey(1500)

                print(f"\n✓ ĐĂNG KÝ THÀNH CÔNG: {name} (MSSV: {student_id})")
                print(f"  - Số ảnh mẫu đã lưu: {len(collected_faces)}")
                print(f"  - Đã lưu thông tin vào: {face_manager.students_file}")
                print(f"  - Đã cập nhật mô hình nhận diện: {face_manager.model_file}\n")
                registered = True
                break

    finally:
        detector.close()
        cap.release()
        cv2.destroyAllWindows()

    return registered


def main() -> None:
    print("=" * 60)
    print("           STAGE 5: ĐĂNG KÝ KHUÔN MẶT MỚI")
    print("=" * 60)

    face_manager = get_face_manager()
    print(f"Số sinh viên hiện có trong dữ liệu: {len(face_manager.students)}")

    while True:
        try:
            name = input("\nNhập Họ và tên (hoặc 'q' để thoát): ").strip()
            if not name or name.lower() == "q":
                print("Thoát chức năng đăng ký.")
                break

            student_id = input("Nhập MSSV / ID: ").strip()
            if not student_id or student_id.lower() == "q":
                print("Thoát chức năng đăng ký.")
                break

            if student_id in face_manager.students:
                print(
                    f"[CHÚ Ý] MSSV '{student_id}' đã tồn tại với tên '{face_manager.students[student_id]}'."
                )
                choice = input("Bạn có muốn ghi đè khuôn mặt mới không? (y/n): ").strip().lower()
                if choice != "y":
                    continue

            ok = register_face(student_id=student_id, name=name)
            if ok:
                more = input("Bạn có muốn đăng ký thêm người khác không? (y/n): ").strip().lower()
                if more != "y":
                    break
        except (KeyboardInterrupt, EOFError):
            print("\nĐã hủy.")
            break


if __name__ == "__main__":
    main()
