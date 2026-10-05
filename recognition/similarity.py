"""Cosine similarity và Euclidean distance trên vector embedding.

Hai ảnh khuôn mặt không nên so sánh pixel-by-pixel:
ánh sáng, góc mặt, background làm pixel khác nhau dù cùng một người.

Face embedding biến khuôn mặt thành vector số (128 hoặc 512 chiều).
Cùng một người → hai vector gần nhau. Người khác → xa nhau.
"""

from __future__ import annotations

import numpy as np


def l2_normalize(vec: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    vec = np.asarray(vec, dtype=np.float32).reshape(-1)
    norm = float(np.linalg.norm(vec))
    if norm < eps:
        return vec
    return vec / norm


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Giá trị trong [-1, 1]. Càng gần 1 càng giống."""
    a_n = l2_normalize(a)
    b_n = l2_normalize(b)
    return float(np.dot(a_n, b_n))


def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    """0 = giống hệt (sau khi chuẩn hóa)."""
    return 1.0 - cosine_similarity(a, b)


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    a_n = l2_normalize(a)
    b_n = l2_normalize(b)
    return float(np.linalg.norm(a_n - b_n))
