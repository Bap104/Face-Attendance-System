# Cơ sở lý thuyết (đưa vào Chương 2 báo cáo)

Tài liệu này là **kiến thức lý thuyết**. Code nằm trong `detection/`, `recognition/`, `scripts/`.

---

## Computer Vision (thị giác máy tính)

Máy tính không “nhìn” như người. Ảnh là ma trận số (pixel). Bài toán CV biến ma trận đó thành thông tin: có mặt không, đó là ai, mắt đang chớp không.

Trong điểm danh: luồng số hóa khuôn mặt từ pixel → hộp mặt → vector đặc trưng → quyết định danh tính.

---

## Face Detection ≠ Face Recognition

| | Detection | Recognition |
|--|-----------|-------------|
| Câu hỏi | *Ở đâu có mặt?* | *Mặt này là ai?* |
| Đầu ra | (x, y, w, h) | MSSV / tên / Unknown |
| Ví dụ | Haar, MediaPipe, RetinaFace | FaceNet, ArcFace/InsightFace |

Nhầm hai khái niệm này là lỗi phổ biến khi viết báo cáo.

---

## A. Haar Cascade

**Là gì.** Bộ phân loại xếp tầng (Viola–Jones, 2001) dùng đặc trưng chữ nhật Haar-like để phát hiện vật thể, phổ biến nhất là mặt thẳng, nhìn camera.

**Haar-like features.** Cửa sổ nhỏ quét ảnh. Tính hiệu số tổng pixel vùng sáng trừ vùng tối (ví dụ: vùng mắt thường tối hơn má). Nhiều kiểu: cạnh ngang/dọc, đường, bốn hình chữ nhật.

**Integral Image.** Bảng tổng tiền tố 2D. Tổng một hình chữ nhật tính bằng 4 phép cộng, không cần cộng từng pixel. Đó là lý do Haar chạy được realtime trên CPU yếu.

**AdaBoost.** Có hàng chục nghìn đặc trưng. AdaBoost chọn vài trăm đặc trưng “ăn tiền” nhất, ghép thành classifier mạnh từ nhiều classifier yếu.

**Cascade Classifier.** Nhiều tầng: tầng đầu rất nhanh, loại vùng chắc chắn không phải mặt. Chỉ vùng khả nghi mới qua tầng sau (đắt hơn). Hầu hết cửa sổ nền bị loại sớm.

**OpenCV.** File XML sẵn: `haarcascade_frontalface_default.xml`. `detectMultiScale` trượt cửa sổ đa tỷ lệ.

**Ưu.** Dễ, có sẵn OpenCV, nhanh CPU, dễ giải thích trong đồ án.

**Nhược.** Yếu khi mặt nghiêng, đeo khẩu trang, ánh sáng xấu; nhiều dương tính giả; **không** cho embedding nên **không** nhận diện danh tính.

**Khi nào dùng trong điểm danh.** Bài lab đầu, slide giải thích detection. Không dùng làm nhận diện chính thức.

---

## B. FaceNet

**Là gì.** Mạng CNN (Google, 2015) ánh xạ khuôn mặt đã crop/align thành vector 128 chiều (bản gốc).

**Face embedding.** Vector số biểu diễn “dáng mặt” đã được học. Cùng người → gần nhau trong không gian vector.

**Vì sao không so pixel.** Cùng một người: khác ánh sáng, góc, tóc, background → pixel khác hoàn toàn. So histogram/pixel không ổn định.

**Triplet Loss.** Mỗi lần học lấy 3 ảnh:
- Anchor: người A
- Positive: ảnh khác của A
- Negative: người B

Mục tiêu: `||f(A) - f(A')|| + margin < ||f(A) - f(B)||`

**So sánh.** Euclidean trên vector đã L2-normalize, hoặc cosine similarity (tương đương gần khi đã chuẩn hóa).

**Pipeline.** Detect → align (mắt ngang) → embedding → so khoảng cách với gallery.

**Trong đồ án.** Dùng FaceNet để *giải thích* embedding và triplet. Triển khai thực tế trên Mac: InsightFace (ArcFace), cùng pipeline.

Chạy minh họa số (không cần ảnh):

```bash
python -m recognition.facenet_demo
```

---

## C. MediaPipe

**Là gì.** Khung ML realtime của Google (mobile/web/desktop): Face Detection, Face Mesh, Hands, Pose.

**Face Detection.** BlazeFace: hộp mặt + vài điểm (mắt, mũi, miệng) rất nhanh trên webcam.

**Face Mesh.** 468 landmark (refine iris thêm điểm mắt).

**Landmark dùng để:**
- Căn chỉnh mặt (xoay 2 mắt nằm ngang) trước khi đưa vào mạng nhận diện
- Ước lượng tư thế đầu (yaw/pitch)
- Liveness đơn giản: EAR (tỷ lệ mở mắt) phát hiện chớp mắt — ảnh in không chớp

**Trong điểm danh.** Detection + alignment + hỗ trợ anti-spoofing mức đồ án. Không thay ArcFace để phân biệt sinh viên.

---

## D. InsightFace

**Là gì.** Bộ thư viện nhận diện mã nguồn mở (detection + recognition) dùng nhiều trong sản phẩm.

**ArcFace.** Hàm mất mát (Deng et al., 2019) học embedding sao cho các lớp (người) tách theo góc trên hypersphere. Thường tốt hơn triplet thuần khi có nhiều identity.

**Quy trình.** SCRFD/RetinaFace detect → align 5 điểm → embedding 512 chiều → cosine similarity với từng sinh viên đã đăng ký.

**Vì sao phù hợp thực tế.** Model pretrained mạnh, API `FaceAnalysis` gọn, chạy ONNX (CPU Mac được), có bản nhẹ `buffalo_sc`.

**So với FaceNet.** Cùng ý tưởng embedding; ArcFace thường chính xác hơn trên bộ lớn; InsightFace dễ triển khai 2024–2026 hơn FaceNet/TensorFlow gốc.

---

## Embedding, threshold, người lạ, nhiều mặt

**Threshold.** Ngưỡng similarity. `sim >= T` → gán danh tính; không thì **Unknown**.

T không lấy từ internet rồi khóa cứng. Đo trên dữ liệu lớp:
- Cặp ảnh cùng sinh viên → phân bố similarity (genuine)
- Cặp khác sinh viên → impostor
- Chọn T cân bằng FAR (nhận nhầm người) và FRR (từ chối người đúng)

**Người lạ.** Không có embedding đủ gần → luôn hiện `Unknown`, không ghi điểm danh.

**Hạn chế nhận nhầm.** Ảnh đăng ký đa góc/ánh sáng; align trước embed; T hơi cao hơn (chấp nhận FRR); không lấy mặt quá nhỏ/nhoà; cooldown điểm danh.

**Nhiều mặt.** Detect tất cả hộp → crop từng mặt → embed từng mặt → match độc lập (lớp học).

---

## Anti-spoofing (lý thuyết, giai đoạn sau MVP)

Ảnh/video trên điện thoại có thể đánh lừa hệ thống chỉ so embedding.

Liveness: chứng minh có người thật (chớp mắt, depth, texture moiré, model chuyên anti-spoof).

MediaPipe mesh + EAR: bài lab tốt nhưng bị video replay đánh lừa.

Nâng cấp: Silent-Face-Anti-Spoofing, MiniFASNet, RGB-anti-spoof của InsightFace.

---

## Đánh giá (Chương 5)

- Accuracy / Precision / Recall / F1 trên tập ảnh cầm-nắm (không chỉ webcam vui)
- FAR = nhận nhầm / số lần impostor
- FRR = từ chối nhầm / số lần genuine
- Latency ms/frame và FPS (`time.perf_counter` quanh vòng lặp)

Test set: người trong gallery, người ngoài gallery, ánh sáng yếu, mặt nghiêng, 2 người cùng frame.
