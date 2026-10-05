"""Demo InsightFace — CHỈ chạy từ Giai đoạn 6, sau khi Haar/MediaPipe ổn.

InsightFace = bộ công cụ nhận diện thực tế:
  RetinaFace/SCRFD (detect) → alignment → ArcFace embedding → cosine similarity.

buffalo_sc: nhẹ, phù hợp MacBook học tập.
buffalo_l: chính xác hơn, chậm hơn.
"""

from __future__ import annotations

import sys

import cv2
from insightface.app import FaceAnalysis

from recognition.similarity import cosine_similarity, l2_normalize


def load_app() -> FaceAnalysis:
    # Apple Silicon: dùng CPU (hoặc CoreML nếu ONNX Runtime hỗ trợ).
    # Không dùng CUDA.
    app = FaceAnalysis(name="buffalo_sc", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app


def embedding_of(app: FaceAnalysis, image_path: str):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(image_path)
    faces = app.get(img)
    if not faces:
        raise ValueError(f"Không phát hiện khuôn mặt: {image_path}")
    faces.sort(key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]), reverse=True)
    return l2_normalize(faces[0].normed_embedding)


def main() -> None:
    if len(sys.argv) != 3:
        print("Cách dùng: python -m recognition.insightface_demo anh1.jpg anh2.jpg")
        sys.exit(1)
    app = load_app()
    e1 = embedding_of(app, sys.argv[1])
    e2 = embedding_of(app, sys.argv[2])
    sim = cosine_similarity(e1, e2)
    print(f"Cosine similarity = {sim:.4f}")
    print("Cùng một người: similarity thường cao hơn ngưỡng bạn chọn.")
    print("Người lạ / khác người: thấp hơn ngưỡng → Unknown.")


if __name__ == "__main__":
    main()
