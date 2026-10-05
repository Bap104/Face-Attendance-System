"""Điểm vào dự án Hệ thống Nhận diện Khuôn mặt & Điểm danh Tự động.

Cách chạy theo từng giai đoạn:
  python main.py --stage 1   Giai đoạn 1: Kiểm tra môi trường
  python main.py --stage 2   Giai đoạn 2: Kiểm tra webcam
  python main.py --stage 3   Giai đoạn 3: Phát hiện khuôn mặt (Haar Cascade - GỐC)
  python main.py --stage 4   Giai đoạn 4: MediaPipe Face & Landmark (GỐC)
  python main.py --stage 5   Giai đoạn 5: [ĐĂNG KÝ KHUÔN MẶT] (Nhập thông tin & chụp mẫu)
  python main.py --stage 6   Giai đoạn 6: [ĐIỂM DANH TỰ ĐỘNG] (Nhận diện realtime & ghi có mặt)
  python main.py --stage 7   Giai đoạn 7: [LỊCH SỬ ĐIỂM DANH] (Xem bảng lịch sử điểm danh)
  python main.py --stage 8   Giai đoạn 8: [SỬA NGƯỜI ĐÃ ĐĂNG KÝ]
  python main.py --stage 9   Giai đoạn 9: [XÓA NGƯỜI ĐÃ ĐĂNG KÝ]

Hoặc chạy trực tiếp không tham số để mở Menu lựa chọn:
  python main.py
"""

from __future__ import annotations

import argparse
import sys


def print_menu() -> None:
    print("=" * 70)
    print("       HỆ THỐNG NHẬN DIỆN KHUÔN MẶT & ĐIỂM DANH TỰ ĐỘNG")
    print("=" * 70)
    print("  [CÁC CHỨC NĂNG GỐC CỦA DỰ ÁN]")
    print("    1. Stage 1: Kiểm tra môi trường")
    print("    2. Stage 2: Kiểm tra camera webcam")
    print("    3. Stage 3: Phát hiện khuôn mặt bằng Haar Cascade (Gốc)")
    print("    4. Stage 4: MediaPipe Face Detection + Landmark Mesh (Gốc)")
    print()
    print("  [HỆ THỐNG ĐĂNG KÝ & ĐIỂM DANH MỚI]")
    print("    5. Stage 5: ĐĂNG KÝ KHUÔN MẶT MỚI (Lưu persistent)")
    print("    6. Stage 6: ĐIỂM DANH KHUÔN MẶT TỰ ĐỘNG REALTIME")
    print("    7. Stage 7: XEM LỊCH SỬ ĐIỂM DANH")
    print("    8. Stage 8: SỬA NGƯỜI ĐÃ ĐĂNG KÝ KHUÔN MẶT")
    print("    9. Stage 9: XÓA NGƯỜI ĐÃ ĐĂNG KÝ KHUÔN MẶT")
    print()
    print("    Q. Thoát")
    print("-" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(description="Face Attendance — chạy theo giai đoạn")
    parser.add_argument(
        "--stage",
        type=int,
        required=False,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        help="Chọn giai đoạn chạy (1-4: gốc, 5: Đăng ký, 6: Điểm danh, 7: Lịch sử, 8: Sửa, 9: Xóa)",
    )
    args = parser.parse_args()

    stage = args.stage
    if stage is None:
        print_menu()
        choice = input("Vui lòng nhập lựa chọn (1-9 hoặc Q để thoát): ").strip().lower()
        if choice in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            stage = int(choice)
        elif choice == "q":
            print("Đã thoát chương trình.")
            sys.exit(0)
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 9.")
            sys.exit(1)

    if stage == 1:
        from scripts.stage01_check_env import main as run
    elif stage == 2:
        from scripts.stage02_webcam import main as run
    elif stage == 3:
        from scripts.stage03_haar import main as run
    elif stage == 4:
        from scripts.stage04_mediapipe import main as run
    elif stage == 5:
        from scripts.stage05_register import main as run
    elif stage == 6:
        from scripts.stage06_attendance import main as run
    elif stage == 7:
        from scripts.stage07_history import main as run
    elif stage == 8:
        from scripts.stage08_edit import main as run
    elif stage == 9:
        from scripts.stage09_delete import main as run
    else:
        print(f"Giai đoạn {stage} không tồn tại.")
        sys.exit(1)

    run()


if __name__ == "__main__":
    main()
