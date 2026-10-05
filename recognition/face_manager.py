"""Quản lý dữ liệu khuôn mặt và nhận diện danh tính chính xác.

Đảm bảo:
  - Phân biệt rõ ràng từng người (Người A vs Người B).
  - Có ngưỡng nhận diện (threshold) chặt chẽ: Người lạ / chưa đăng ký -> UNKNOWN.
  - Tuyệt đối không gán tên cố định hay lấy tên người đăng ký trước đó.
  - Lưu trữ persistent vào:
      + data/students.csv
      + data/face_model.yml (mô hình nhận diện)
      + dataset/known_faces/{student_id}/ (ảnh mẫu khuôn mặt)
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
import shutil
import sys

import cv2
import numpy as np

# Đảm bảo nhận diện được thư mục gốc của project
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import DATASET_DIR, DATA_DIR, STUDENTS_CSV


class FaceManager:
    # Ngưỡng nhận diện cho LBPH: khoảng cách càng nhỏ càng giống (cùng người: ~35-55, khác người: >75)
    LBPH_THRESHOLD = 65.0
    # Ngưỡng nhận diện cho NCC Template: độ tương quan càng gần 1 càng giống
    NCC_THRESHOLD = 0.72

    def __init__(self) -> None:
        self.students_file = STUDENTS_CSV
        self.dataset_dir = DATASET_DIR
        self.model_file = DATA_DIR / "face_model.yml"

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.dataset_dir.mkdir(parents=True, exist_ok=True)

        # Danh sách sinh viên: student_id -> name
        self.students: dict[str, str] = {}
        # Ánh xạ label số nguyên sang student_id cho model
        self.label_to_id: dict[int, str] = {}
        self.id_to_label: dict[str, int] = {}

        # Kiểm tra xem OpenCV có module cv2.face (LBPH) hay không
        self.has_lbph = hasattr(cv2, "face") and hasattr(cv2.face, "LBPHFaceRecognizer_create")
        self.recognizer = None
        if self.has_lbph:
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Nạp dữ liệu khi khởi tạo
        self.load_data()

    def load_data(self) -> None:
        """Đọc danh sách sinh viên và nạp mô hình nhận diện đã lưu."""
        self.students.clear()
        self.label_to_id.clear()
        self.id_to_label.clear()

        # 1. Đọc danh sách sinh viên từ students.csv
        if self.students_file.exists():
            try:
                with self.students_file.open("r", newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    idx = 1
                    for row in reader:
                        sid = row.get("student_id", "").strip()
                        name = row.get("name", "").strip()
                        if sid and name:
                            self.students[sid] = name
                            self.label_to_id[idx] = sid
                            self.id_to_label[sid] = idx
                            idx += 1
            except Exception as e:
                print(f"[CẢNH BÁO] Lỗi khi đọc students.csv: {e}")

        # 2. Nạp mô hình nhận diện đã lưu
        if self.has_lbph and self.model_file.exists() and len(self.students) > 0:
            try:
                self.recognizer.read(str(self.model_file))
            except Exception:
                # Nếu file model lỗi hoặc chưa đồng bộ, huấn luyện lại từ dataset
                self.train_model()
        elif len(self.students) > 0:
            self.train_model()

    def train_model(self) -> bool:
        """Huấn luyện mô hình nhận diện từ toàn bộ ảnh trong dataset/known_faces/."""
        if not self.has_lbph:
            return False

        faces: list[np.ndarray] = []
        labels: list[int] = []

        for sid, label in self.id_to_label.items():
            person_dir = self.dataset_dir / sid
            if not person_dir.exists():
                continue

            for img_path in person_dir.glob("*.jpg"):
                img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
                if img is not None and img.size > 0:
                    img = cv2.resize(img, (120, 120))
                    img = cv2.equalizeHist(img)
                    faces.append(img)
                    labels.append(label)

        if len(faces) == 0:
            return False

        try:
            self.recognizer.train(faces, np.array(labels, dtype=np.int32))
            self.recognizer.write(str(self.model_file))
            return True
        except Exception as e:
            print(f"[LỖI] Không huấn luyện được mô hình LBPH: {e}")
            return False

    def save_student(
        self,
        student_id: str,
        name: str,
        face_images: list[np.ndarray],
    ) -> bool:
        """Lưu sinh viên mới: ghi thông tin, lưu chùm ảnh mẫu và cập nhật model."""
        sid = str(student_id).strip()
        sname = str(name).strip()
        if not sid or not sname or len(face_images) == 0:
            return False

        # 1. Cập nhật vào RAM
        self.students[sid] = sname
        if sid not in self.id_to_label:
            new_label = len(self.id_to_label) + 1
            self.id_to_label[sid] = new_label
            self.label_to_id[new_label] = sid

        # 2. Ghi persistent vào students.csv
        headers = ["student_id", "name", "created_at"]
        existing_rows: dict[str, dict] = {}
        if self.students_file.exists():
            try:
                with self.students_file.open("r", newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get("student_id"):
                            existing_rows[row["student_id"]] = row
            except Exception:
                pass

        existing_rows[sid] = {
            "student_id": sid,
            "name": sname,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        with self.students_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for row in existing_rows.values():
                writer.writerow(row)

        # 3. Lưu toàn bộ các ảnh khuôn mặt mẫu vào dataset/known_faces/{student_id}/
        person_dir = self.dataset_dir / sid
        person_dir.mkdir(parents=True, exist_ok=True)
        for i, face_bgr in enumerate(face_images):
            if face_bgr is not None and face_bgr.size > 0:
                img_gray = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2GRAY)
                img_gray = cv2.resize(img_gray, (120, 120))
                img_gray = cv2.equalizeHist(img_gray)
                cv2.imwrite(str(person_dir / f"face_{i + 1:02d}.jpg"), img_gray)

        # 4. Huấn luyện lại mô hình với dữ liệu mới
        self.train_model()
        return True

    def recognize(
        self, face_bgr: np.ndarray, threshold: float | None = None
    ) -> tuple[str, str, float]:
        """Nhận diện khuôn mặt với cơ chế so sánh toàn bộ database và kiểm tra threshold.

        Trả về:
          (student_id, name, score_hoặc_distance)
        Nếu không khớp hoặc điểm không đạt threshold -> ("Unknown", "Unknown", distance)
        """
        if len(self.students) == 0 or face_bgr is None or face_bgr.size == 0:
            return "Unknown", "Unknown", 999.0

        # Tiền xử lý ảnh khuôn mặt
        gray = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (120, 120))
        gray = cv2.equalizeHist(gray)

        # Phương án 1: Dùng mô hình LBPH Face Recognizer
        if self.has_lbph and self.model_file.exists():
            try:
                label_id, distance = self.recognizer.predict(gray)
                t = threshold if threshold is not None else self.LBPH_THRESHOLD

                # Chỉ khi khoảng cách NHỎ HƠN threshold mới xác nhận danh tính
                if distance <= t and label_id in self.label_to_id:
                    sid = self.label_to_id[label_id]
                    sname = self.students.get(sid, sid)
                    return sid, sname, float(distance)
                else:
                    return "Unknown", "Unknown", float(distance)
            except Exception:
                pass

        # Phương án 2 (Fallback): So khớp mẫu chuẩn hóa Normalized Cross-Correlation
        best_sid = "Unknown"
        best_name = "Unknown"
        max_corr = -1.0

        t_ncc = threshold if threshold is not None else self.NCC_THRESHOLD
        query_norm = (gray.astype(np.float32) - np.mean(gray)) / (np.std(gray) + 1e-6)

        for sid in self.students.keys():
            person_dir = self.dataset_dir / sid
            if not person_dir.exists():
                continue

            for img_path in person_dir.glob("*.jpg"):
                ref = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
                if ref is None:
                    continue
                ref_norm = (ref.astype(np.float32) - np.mean(ref)) / (np.std(ref) + 1e-6)
                corr = float(np.mean(query_norm * ref_norm))
                if corr > max_corr:
                    max_corr = corr
                    best_sid = sid
                    best_name = self.students.get(sid, sid)

        if max_corr >= t_ncc:
            return best_sid, best_name, max_corr
        return "Unknown", "Unknown", max_corr

    def _rebuild_labels(self) -> None:
        self.label_to_id.clear()
        self.id_to_label.clear()
        for idx, sid in enumerate(self.students.keys(), start=1):
            self.label_to_id[idx] = sid
            self.id_to_label[sid] = idx

    def _read_student_rows(self) -> dict[str, dict]:
        existing_rows: dict[str, dict] = {}
        if not self.students_file.exists():
            return existing_rows
        try:
            with self.students_file.open("r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sid = (row.get("student_id") or "").strip()
                    if sid:
                        existing_rows[sid] = row
        except Exception:
            pass
        return existing_rows

    def _write_student_rows(self, rows: dict[str, dict]) -> None:
        headers = ["student_id", "name", "created_at"]
        with self.students_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for row in rows.values():
                writer.writerow(
                    {
                        "student_id": row.get("student_id", ""),
                        "name": row.get("name", ""),
                        "created_at": row.get("created_at", ""),
                    }
                )

    def _sync_model_after_identity_change(self) -> None:
        self._rebuild_labels()
        if len(self.students) == 0:
            if self.model_file.exists():
                try:
                    self.model_file.unlink()
                except OSError:
                    pass
            if self.has_lbph:
                self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            return
        self.train_model()

    def delete_student(self, student_id: str) -> tuple[bool, str]:
        """Xóa người theo MSSV/ID: CSV + ảnh mẫu + model. Không đụng attendance.csv."""
        sid = str(student_id).strip()
        if not sid:
            return False, "MSSV/ID trống."
        if sid not in self.students:
            return False, f"Không tìm thấy người với MSSV/ID '{sid}'."

        name = self.students.pop(sid)
        rows = self._read_student_rows()
        rows.pop(sid, None)
        self._write_student_rows(rows)

        person_dir = self.dataset_dir / sid
        if person_dir.exists():
            shutil.rmtree(person_dir, ignore_errors=True)

        self._sync_model_after_identity_change()
        return True, f"Đã xóa {name} (MSSV/ID: {sid})."

    def update_student(
        self,
        old_student_id: str,
        new_student_id: str | None = None,
        new_name: str | None = None,
    ) -> tuple[bool, str]:
        """Sửa MSSV/ID và/hoặc họ tên. Đổi ID thì đổi luôn thư mục ảnh. Không đụng attendance.csv."""
        old_sid = str(old_student_id).strip()
        if not old_sid or old_sid not in self.students:
            return False, f"Không tìm thấy người với MSSV/ID '{old_sid}'."

        new_sid = old_sid if new_student_id is None else str(new_student_id).strip()
        new_sname = (
            self.students[old_sid] if new_name is None else str(new_name).strip()
        )
        if not new_sid or not new_sname:
            return False, "MSSV/ID và họ tên không được để trống."

        if new_sid != old_sid and new_sid in self.students:
            return False, f"MSSV/ID '{new_sid}' đã tồn tại. Không thể trùng ID."

        if new_sid == old_sid and new_sname == self.students[old_sid]:
            return True, "Không có thay đổi thông tin."

        old_name = self.students[old_sid]
        rows = self._read_student_rows()
        old_row = rows.pop(old_sid, {})
        created_at = old_row.get("created_at") or datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        if new_sid != old_sid:
            old_dir = self.dataset_dir / old_sid
            new_dir = self.dataset_dir / new_sid
            if old_dir.exists():
                if new_dir.exists():
                    return False, f"Thư mục ảnh của MSSV/ID '{new_sid}' đã tồn tại."
                try:
                    old_dir.rename(new_dir)
                except OSError as e:
                    return False, f"Không đổi được thư mục ảnh: {e}"
            self.students.pop(old_sid)
            self.students[new_sid] = new_sname
        else:
            self.students[old_sid] = new_sname

        rows[new_sid] = {
            "student_id": new_sid,
            "name": new_sname,
            "created_at": created_at,
        }
        self._write_student_rows(rows)
        self._sync_model_after_identity_change()
        return True, f"Đã cập nhật {old_name} ({old_sid}) → {new_sname} ({new_sid})."


_default_face_manager: FaceManager | None = None


def get_face_manager() -> FaceManager:
    global _default_face_manager
    if _default_face_manager is None:
        _default_face_manager = FaceManager()
    return _default_face_manager
