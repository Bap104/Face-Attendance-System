"""Minh họa ý tưởng FaceNet: embedding + so sánh khoảng cách.

FaceNet (Schroff et al., 2015) học không gian embedding bằng Triplet Loss:
  - Anchor: ảnh người A
  - Positive: ảnh khác của cùng người A
  - Negative: ảnh người B

Mục tiêu: distance(anchor, positive) + margin < distance(anchor, negative)

Demo này có 2 chế độ:
1) Luôn chạy được: so sánh 2 vector giả lập (dạy toán embedding).
2) Tùy chọn: nếu cài insightface, dùng embedding thật từ 2 ảnh.

Không nên bắt buộc TensorFlow/FaceNet gốc trên Apple Silicon ở giai đoạn đầu
(cài đặt nặng, dễ lỗi). InsightFace/ArcFace là bản thực tế hơn cho MVP.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from recognition.similarity import cosine_similarity, euclidean_distance, l2_normalize


def fake_triplet_example() -> None:
    rng = np.random.default_rng(42)
    # Giả lập embedding 128 chiều giống FaceNet gốc
    anchor = l2_normalize(rng.normal(size=128))
    # Positive gần anchor (cùng người, nhiễu nhỏ)
    positive = l2_normalize(anchor + rng.normal(scale=0.05, size=128))
    # Negative khác hẳn
    negative = l2_normalize(rng.normal(size=128))

    print("=== FaceNet / Triplet Loss (minh họa số) ===")
    print(f"cos(anchor, positive) = {cosine_similarity(anchor, positive):.4f}  (cùng người → cao)")
    print(f"cos(anchor, negative) = {cosine_similarity(anchor, negative):.4f}  (khác người → thấp)")
    print(f"L2(anchor, positive)  = {euclidean_distance(anchor, positive):.4f}")
    print(f"L2(anchor, negative)  = {euclidean_distance(anchor, negative):.4f}")
    print()
    print("Triplet Loss muốn: L2(anchor, positive) + margin < L2(anchor, negative)")


def compare_two_images_with_insightface(image_a: str, image_b: str) -> None:
    """Embedding thật. Chạy sau khi đã cài insightface + onnxruntime."""
    import cv2
    from insightface.app import FaceAnalysis

    app = FaceAnalysis(name="buffalo_sc", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(640, 640))

    def embed(path: str) -> np.ndarray:
        img = cv2.imread(path)
        if img is None:
            raise FileNotFoundError(path)
        faces = app.get(img)
        if not faces:
            raise ValueError(f"Không thấy khuôn mặt trong {path}")
        faces = sorted(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]), reverse=True)
        return l2_normalize(faces[0].normed_embedding)

    ea, eb = embed(image_a), embed(image_b)
    sim = cosine_similarity(ea, eb)
    print("=== So sánh 2 ảnh bằng embedding (InsightFace, cùng ý tưởng FaceNet) ===")
    print(f"Ảnh A: {image_a}")
    print(f"Ảnh B: {image_b}")
    print(f"Cosine similarity = {sim:.4f}")
    print("Cùng người thường > 0.4 ~ 0.6 (phải tự đo). Khác người thường thấp hơn.")


if __name__ == "__main__":
    import sys

    fake_triplet_example()
    if len(sys.argv) == 3:
        compare_two_images_with_insightface(sys.argv[1], sys.argv[2])
    else:
        print()
        print("Để so sánh 2 ảnh thật (giai đoạn 6, cần insightface):")
        print("  python -m recognition.facenet_demo path_a.jpg path_b.jpg")
