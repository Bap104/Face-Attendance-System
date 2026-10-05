"""Giai đoạn 7: Xem và quản lý lịch sử điểm danh.

Chức năng:
  - Đọc dữ liệu persistent từ data/attendance.csv.
  - Hiển thị danh sách điểm danh rõ ràng theo bảng (MSSV, Họ tên, Ngày, Giờ, Trạng thái).
  - Thống kê tổng số lượt điểm danh và số người đã điểm danh hôm nay.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
import sys

# Đảm bảo nhận diện được thư mục gốc khi chạy trực tiếp
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import ATTENDANCE_CSV, STUDENTS_CSV


def main() -> None:
    print("=" * 75)
    print("                 STAGE 7: LỊCH SỬ ĐIỂM DANH")
    print("=" * 75)

    if not ATTENDANCE_CSV.exists():
        print(f"\n[THÔNG BÁO] Chưa có dữ liệu điểm danh (file {ATTENDANCE_CSV} chưa có).")
        print("Vui lòng chạy Stage 6 để thực hiện điểm danh trước.\n")
        return

    records = []
    with ATTENDANCE_CSV.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    if len(records) == 0:
        print("\n[THÔNG BÁO] File điểm danh hiện đang trống, chưa có bản ghi nào.\n")
        return

    today = datetime.now().strftime("%d/%m/%Y")
    today_count = sum(1 for r in records if r.get("date") == today)

    print(f"\nTổng số bản ghi điểm danh : {len(records)}")
    print(f"Số lượt điểm danh hôm nay ({today}): {today_count}\n")

    # In bảng dữ liệu
    print(f"{'STT':<5} | {'MSSV / ID':<12} | {'HỌ VÀ TÊN':<25} | {'NGÀY':<12} | {'GIỜ':<10} | {'TRẠNG THÁI'}")
    print("-" * 75)

    for i, r in enumerate(records, start=1):
        sid = r.get("student_id", "")
        name = r.get("name", "")
        date = r.get("date", "")
        time_str = r.get("time", "")
        status = r.get("status", "")
        print(f"{i:<5} | {sid:<12} | {name:<25} | {date:<12} | {time_str:<10} | {status}")

    print("-" * 75)
    print(f"Dữ liệu được lưu persistent tại: {ATTENDANCE_CSV}\n")


if __name__ == "__main__":
    main()
