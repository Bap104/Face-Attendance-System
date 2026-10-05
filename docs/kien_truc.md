# Kiến trúc hệ thống điểm danh

Đây là phần **thiết kế** (báo cáo Chương 3). Code MVP hiện mới có Camera + Detection.

```
[Webcam]
    |
    v
[Face Detection]     Haar (học) / MediaPipe hoặc SCRFD (thực tế)
    |
    v
[Alignment]          MediaPipe landmarks / 5-point InsightFace
    |
    v
[Embedding]          ArcFace (InsightFace); FaceNet để hiểu lý thuyết
    |
    v
[So sánh gallery]    cosine similarity, max score
    |
    v
[Quyết định]         score >= T ? (tên, MSSV) : Unknown
    |
    v
[Chống trùng]        đã có bản ghi cùng MSSV + cùng ngày? 
    |
    v
[Ghi attendance]     CSV (MVP) → SQLite (nâng cấp)
    |
    v
[Hiển thị]           khung + chữ trên frame; sau này GUI
```

## Vai trò từng khối trong buổi điểm danh

1. **Camera** lấy frame 30 FPS.
2. **Detection** tìm mọi mặt trong lớp (nhiều hộp).
3. **Alignment** xoay/crop mặt chuẩn, giảm lỗi do nghiêng đầu.
4. **Recognition** biến crop thành vector, không lưu cả ảnh lúc so khớp.
5. **Database** gallery embedding lúc đăng ký; bảng Attendance lúc điểm danh.
6. **Cooldown/unique ngày** tránh 100 dòng “Nguyễn Văn A” vì đứng 3 phút trước camera.
7. **UI** giáo viên thấy Unknown vs đã điểm danh.

## Gắn 4 công nghệ vào đúng chỗ

- **Haar:** demo detection, không đưa vào đường nhận diện chính.
- **MediaPipe:** detection realtime + landmark alignment + (sau) chớp mắt.
- **FaceNet:** chương lý thuyết embedding; không bắt buộc chạy TensorFlow trên Mac.
- **InsightFace:** khối recognition chính của sản phẩm MVP nâng cấp.
