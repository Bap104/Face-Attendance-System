"""Điểm danh ghi CSV — dễ đọc, phù hợp MVP.

Mỗi dòng: student_id, name, date, time, status
Không ghi trùng cùng student_id trong cùng một ngày.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
import sys

# Đảm bảo nhận diện được thư mục gốc khi chạy trực tiếp: python attendance/csv_store.py
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import ATTENDANCE_CSV, DATA_DIR


class CsvAttendanceStore:
    HEADERS = ["student_id", "name", "date", "time", "status"]

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or ATTENDANCE_CSV
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with self.path.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(self.HEADERS)

    def already_marked_today(self, student_id: str) -> bool:
        if not self.path.exists():
            return False
        sid = str(student_id).strip()
        today_dmy = datetime.now().strftime("%d/%m/%Y")
        today_ymd = datetime.now().strftime("%Y-%m-%d")
        with self.path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("student_id") == sid and row.get("date") in (today_dmy, today_ymd):
                    return True
        return False

    def mark(self, student_id: str, name: str, status: str = "PRESENT") -> dict | None:
        """Tự động điểm danh khi nhận diện được người.

        Quy tắc:
        - Người Unknown hoặc để trống -> tuyệt đối không điểm danh.
        - Đã điểm danh hôm nay -> không tạo bản ghi mới (trả về None).
        - Chưa điểm danh hôm nay -> tự động ghi nhận điểm danh.
        """
        if not student_id or not name:
            return None
        sid = str(student_id).strip()
        sname = str(name).strip()
        if sid.lower() == "unknown" or sname.lower() == "unknown":
            return None

        if self.already_marked_today(sid):
            return None

        now = datetime.now()
        record = {
            "student_id": sid,
            "name": sname,
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M:%S"),
            "status": status,
        }
        with self.path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.HEADERS)
            writer.writerow(record)
        return record

    def auto_mark(self, student_id: str, name: str, status: str = "PRESENT") -> dict | None:
        """Tự động điểm danh sinh viên đã nhận diện (alias cho mark)."""
        return self.mark(student_id=student_id, name=name, status=status)


_default_store: CsvAttendanceStore | None = None


def get_attendance_store() -> CsvAttendanceStore:
    global _default_store
    if _default_store is None:
        _default_store = CsvAttendanceStore()
    return _default_store


def auto_mark_attendance(student_id: str, name: str, status: str = "PRESENT") -> dict | None:
    """Chức năng điểm danh tự động khi nhận diện thành công một người.

    Quy trình:
    Face Detection -> Face Recognition -> Nhận diện được người ->
    Kiểm tra đã điểm danh hôm nay chưa:
      - Chưa: Tự động điểm danh (lưu MSSV/ID, Họ tên, Ngày, Thời gian, Trạng thái)
      - Đã rồi: Không tạo bản ghi mới (trả về None)
      - Người Unknown: Tuyệt đối không điểm danh
    """
    return get_attendance_store().mark(student_id=student_id, name=name, status=status)


if __name__ == "__main__":
    print("=== DEMO CHỨC NĂNG ĐIỂM DANH TỰ ĐỘNG ===")
    
    # 1. Nhận diện người trong danh sách (lần đầu trong ngày)
    print("\n1. Nhận diện Nguyễn Văn A (MSSV: 22123456) lần đầu trong ngày:")
    res1 = auto_mark_attendance("22123456", "Nguyễn Văn A")
    if res1:
        print(f"   -> [THÀNH CÔNG] Đã tự động điểm danh: {res1}")
    else:
        print("   -> [BỎ QUA] Đã được điểm danh hôm nay rồi.")

    # 2. Người đó xuất hiện lại trong ngày
    print("\n2. Nguyễn Văn A tiếp tục đứng trước camera (xuất hiện lại):")
    res2 = auto_mark_attendance("22123456", "Nguyễn Văn A")
    if res2:
        print(f"   -> [LỖI] Tạo bản ghi trùng: {res2}")
    else:
        print("   -> [BỎ QUA] Người này đã điểm danh hôm nay rồi, không tạo bản ghi mới.")

    # 3. Người lạ / Unknown
    print("\n3. Người lạ (Unknown) đứng trước camera:")
    res3 = auto_mark_attendance("Unknown", "Unknown")
    if res3:
        print(f"   -> [LỖI] Đã điểm danh người lạ: {res3}")
    else:
        print("   -> [CHẶN] Tuyệt đối không điểm danh người Unknown.")

    print(f"\nDữ liệu điểm danh được lưu tại: {ATTENDANCE_CSV}")
