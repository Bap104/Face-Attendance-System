# So sánh 4 công nghệ (bảng báo cáo / slide)

| Công nghệ | Mục đích | Độ chính xác | Tốc độ | Độ khó | Ưu điểm | Nhược điểm | Vai trò trong dự án |
|-----------|----------|--------------|--------|--------|---------|------------|---------------------|
| Haar Cascade | Phát hiện mặt (detection) | Thấp–trung bình, kém mặt nghiêng | Rất nhanh CPU | Thấp | Có sẵn OpenCV, dễ giảng | Nhiều false box, không nhận diện ai | Lab đầu, giải thích Viola–Jones |
| MediaPipe | Detection + 468 landmark | Detection tốt webcam | Rất nhanh | Thấp–trung bình | Realtime, alignment, hỗ trợ liveness đơn giản | Không phải face ID | Detect/align trên webcam lớp |
| FaceNet | Recognition bằng embedding | Tốt (model gốc 2015) | Trung bình | Cao (TF trên Mac khó) | Nền tảng triplet/embedding | Cài đặt nặng, API cũ | Lý thuyết Chương 2, so sánh |
| InsightFace (ArcFace) | Detection + recognition thực tế | Cao | Nhanh trên CPU (bản sc) | Trung bình | Pretrained mạnh, ONNX, gallery cosine | Cần hiểu threshold; model tải lần đầu | Khối nhận diện chính thức |

## Ví dụ trong chính hệ thống điểm danh

**Sáng thứ 2, camera cửa lớp.**

1. Haar vẽ nhầm ô lên balo → nếu tin Haar để điểm danh sẽ sai. Haar chỉ để bạn *học* detection.
2. MediaPipe cho hộp mặt ổn định + điểm 2 mắt. Bạn xoay crop cho thẳng rồi mới nhận diện.
3. FaceNet giải thích vì sao lưu 512 số/người thay vì 50 ảnh JPEG.
4. InsightFace so vector sinh viên A với gallery: 0.72 vs ngưỡng 0.45 → “Nguyễn Văn A – 123456”. Sinh viên không có trong lớp: 0.21 → **Unknown**, không ghi CSV.

Không dùng Haar để phân biệt hai sinh viên. Không dùng MediaPipe mesh làm “vân mặt”. Không cần FaceNet và InsightFace cùng lúc trên đường realtime (trùng vai trò).
