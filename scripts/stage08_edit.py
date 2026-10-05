"""Giai đoạn 8: Sửa thông tin người đã đăng ký khuôn mặt.

Cho phép sửa Họ tên, MSSV/ID và (tuỳ chọn) chụp lại khuôn mặt
bằng đúng quy trình camera của Stage 5. Không đụng lịch sử điểm danh.
"""

from __future__ import annotations

from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from recognition.face_manager import get_face_manager
from scripts.stage05_register import register_face


def _print_list(face_manager) -> list[tuple[str, str]]:
    people = list(face_manager.students.items())
    if not people:
        print("\n[THÔNG BÁO] Chưa có người nào được đăng ký khuôn mặt.")
        print("Vui lòng chạy Stage 5 để đăng ký trước.\n")
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
    print("        STAGE 8: SỬA NGƯỜI ĐÃ ĐĂNG KÝ KHUÔN MẶT")
    print("=" * 60)

    face_manager = get_face_manager()

    while True:
        people = _print_list(face_manager)
        if not people:
            return

        choice = input(
            "\nNhập STT hoặc MSSV/ID cần sửa (hoặc 'q' để thoát): "
        ).strip()
        if not choice or choice.lower() == "q":
            print("Thoát chức năng sửa.")
            return

        sid = _resolve_selection(choice, people)
        if sid is None:
            print("[LỖI] Không tìm thấy người. Hãy nhập đúng STT hoặc MSSV/ID.")
            continue

        old_name = face_manager.students[sid]
        print(f"\nĐang sửa: {old_name} (MSSV/ID: {sid})")
        print("Để trống và Enter nếu muốn giữ nguyên giá trị cũ.")

        new_name = input(f"Họ tên mới [{old_name}]: ").strip()
        new_sid = input(f"MSSV/ID mới [{sid}]: ").strip()
        recapture = input("Cập nhật lại khuôn mặt? (y/n): ").strip().lower() == "y"

        final_name = new_name or old_name
        final_sid = new_sid or sid

        confirm = input(
            f"Xác nhận lưu: {final_name} (MSSV/ID: {final_sid})? (y/n): "
        ).strip().lower()
        if confirm != "y":
            print("Đã hủy, không thay đổi dữ liệu.")
            continue

        ok, message = face_manager.update_student(
            old_student_id=sid,
            new_student_id=final_sid,
            new_name=final_name,
        )
        print(message)
        if not ok:
            continue

        if recapture:
            print("\nMở camera để cập nhật khuôn mặt (SPACE/S = chụp, Q = hủy)...")
            registered = register_face(student_id=final_sid, name=final_name)
            if registered:
                print("Đã cập nhật khuôn mặt thành công.")
            else:
                print("Không cập nhật khuôn mặt (hủy hoặc lỗi camera). Thông tin vẫn đã lưu.")

        print("\nDanh sách sau khi sửa:")
        _print_list(face_manager)

        more = input("Sửa thêm người khác? (y/n): ").strip().lower()
        if more != "y":
            return


if __name__ == "__main__":
    main()
