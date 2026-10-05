"""Giai đoạn 9: Xóa người đã đăng ký khuôn mặt.

Xóa theo MSSV/ID (không xóa theo tên). Xóa students.csv + ảnh mẫu + model.
Không xóa lịch sử điểm danh trong data/attendance.csv.
"""

from __future__ import annotations

from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from recognition.face_manager import get_face_manager


def _print_list(face_manager) -> list[tuple[str, str]]:
    people = list(face_manager.students.items())
    if not people:
        print("\n[THÔNG BÁO] Chưa có người nào được đăng ký khuôn mặt.")
        print("Không có dữ liệu để xóa.\n")
        return []
    print(f"\n{'STT':<5} | {'MSSV / ID':<12} | {'HỌ VÀ TÊN'}")
    print("-" * 50)
    for i, (sid, name) in enumerate(people, start=1):
        print(f"{i:<5} | {sid:<12} | {name}")
    print("-" * 50)
    return people


def _resolve_selection(choice: str, people: list[tuple[str, str]]) -> str | None:
    raw = choice.strip()
    if not raw:
        return None
    ids = {sid for sid, _ in people}
    if raw in ids:
        return raw
    if raw.isdigit():
        idx = int(raw)
        if 1 <= idx <= len(people):
            return people[idx - 1][0]
    return None


def main() -> None:
    print("=" * 60)
    print("        STAGE 9: XÓA NGƯỜI ĐÃ ĐĂNG KÝ KHUÔN MẶT")
    print("=" * 60)

    face_manager = get_face_manager()

    while True:
        people = _print_list(face_manager)
        if not people:
            return

        choice = input(
            "\nNhập STT hoặc MSSV/ID cần xóa (hoặc 'q' để thoát): "
        ).strip()
        if not choice or choice.lower() == "q":
            print("Thoát chức năng xóa.")
            return

        sid = _resolve_selection(choice, people)
        if sid is None:
            print("[LỖI] Không tìm thấy người. Hãy nhập đúng STT hoặc MSSV/ID.")
            continue

        name = face_manager.students[sid]
        confirm = input(
            f"XÁC NHẬN xóa '{name}' (MSSV/ID: {sid})? Không thể hoàn tác. (y/n): "
        ).strip().lower()
        if confirm != "y":
            print("Đã hủy, không xóa.")
            continue

        ok, message = face_manager.delete_student(sid)
        print(message)
        if not ok:
            continue

        print("\nDanh sách sau khi xóa:")
        remaining = _print_list(face_manager)
        if not remaining:
            return

        more = input("Xóa thêm người khác? (y/n): ").strip().lower()
        if more != "y":
            return


if __name__ == "__main__":
    main()
