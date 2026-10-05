# Hệ thống nhận diện khuôn mặt & điểm danh tự động

Chương trình Python mở webcam, nhận diện khuôn mặt realtime, đăng ký người mới và tự động điểm danh lưu vào file CSV. Dữ liệu được lưu trữ lâu dài (persistent), không bị mất khi tắt chương trình.

* **File chạy chính:** `main.py`
* **Hỗ trợ:** Cả **macOS** và **Windows** (kèm Linux).

---

## ⚡ Hướng dẫn cài đặt lần đầu (Chỉ làm 1 lần duy nhất)

### 🍏 Dành cho macOS / Linux (Mở Terminal)

```bash
# Bước 1: Đi vào thư mục chứa code (thay bằng đường dẫn trên máy của bạn)
cd <duong_dan_den_thu_muc_A2_NDKM>

# Bước 2: Tạo môi trường ảo
python3 -m venv .venv

# Bước 3: Kích hoạt môi trường ảo
source .venv/bin/activate

# Bước 4: Cài đặt toàn bộ thư viện
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install opencv-contrib-python

# Bước 5: Kiểm tra môi trường và camera
python main.py --stage 1

# Bước 6: Khởi chạy chương trình chính
python main.py
```

---

### 🪟 Dành cho Windows (Mở PowerShell)

```powershell
# Bước 1: Đi vào thư mục chứa code (thay bằng đường dẫn trên máy của bạn)
cd <duong_dan_den_thu_muc_A2_NDKM>

# Bước 2: Mở quyền chạy script (tránh lỗi bảo mật của Windows PowerShell)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Bước 3: Tạo môi trường ảo
python -m venv .venv

# Bước 4: Kích hoạt môi trường ảo
.venv\Scripts\Activate.ps1

# Bước 5: Cài đặt toàn bộ thư viện
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install opencv-contrib-python

# Bước 6: Kiểm tra môi trường và camera
python main.py --stage 1

# Bước 7: Khởi chạy chương trình chính
python main.py
```

*(Nếu bạn dùng **Command Prompt (CMD)** thay vì PowerShell, tại Bước 4 hãy gõ: `.venv\Scripts\activate.bat`)*

---

## 🔄 Cách chạy từ lần thứ 2 trở đi (Hằng ngày)

Sau khi đã cài đặt xong lần đầu, những lần sau bạn **KHÔNG CẦN** tạo lại venv hay gõ `pip install` nữa. Chỉ cần mở Terminal / PowerShell và gõ **đúng 3 dòng**:

### 🍏 Trên macOS / Linux:
```bash
cd <duong_dan_den_thu_muc_A2_NDKM>
source .venv/bin/activate
python main.py
```

### 🪟 Trên Windows:
```powershell
cd <duong_dan_den_thu_muc_A2_NDKM>
.venv\Scripts\Activate.ps1
python main.py
```
*(Nếu dùng CMD: `.venv\Scripts\activate.bat`)*

> 💡 **Mẹo:** Muốn vào thẳng màn hình điểm danh ngay mà không cần qua Menu, đổi dòng cuối thành:
> ```bash
> python main.py --stage 6
> ```

---

## 💡 Lưu ý về đường dẫn `<duong_dan_den_thu_muc_A2_NDKM>`

* Nếu bạn mở thư mục dự án trực tiếp bằng **VS Code** hoặc **Cursor**:
  - Mở Terminal tích hợp (`Ctrl + ~` hoặc `Cmd + ~`).
  - Nếu Terminal đang ở thư mục ngoài, chỉ cần gõ:
    ```bash
    cd A2_NDKM
    ```
* **Cách kiểm tra bạn đã đứng đúng thư mục chưa:**
  - Trên macOS/Linux gõ `ls`, trên Windows gõ `dir`.
  - Nếu thấy file `main.py` và `requirements.txt` hiện ra là bạn đã ở đúng vị trí!

---

## 🎮 Hướng dẫn sử dụng Menu & Phím bấm

Khi chạy lệnh `python main.py`, bạn nhập số từ **1** đến **9** hoặc **Q** trên bàn phím:

| Lựa chọn | Chức năng | Phím thao tác khi camera mở |
| :---: | :--- | :--- |
| **`1`** | Kiểm tra môi trường & Camera | Tự động kiểm tra |
| **`2`** | Xem thử webcam | Nhấn **`Q`** để tắt |
| **`3`** | Phát hiện mặt bằng Haar Cascade | Nhấn **`Q`** để tắt |
| **`4`** | Phát hiện mặt bằng MediaPipe Mesh | Phím **`D`** (chỉ hiện box), **`M`** (hiện mesh), **`Q`** (thoát) |
| **`5`** | **ĐĂNG KÝ KHUÔN MẶT MỚI** | Nhập Họ tên ➜ Nhập MSSV ➜ Nhìn thẳng camera, bấm **`SPACE`** (hoặc **`S`**) để chụp 15 ảnh mẫu ➜ Bấm **`Q`** để hoàn tất |
| **`6`** | **ĐIỂM DANH TỰ ĐỘNG REALTIME** | Camera tự nhận diện người đã đăng ký và ghi nhận điểm danh vào CSV. Bấm **`Q`** để dừng |
| **`7`** | **XEM LỊCH SỬ ĐIỂM DANH** | In danh sách bảng điểm danh ra màn hình |
| **`8`** | **SỬA THÔNG TIN NGƯỜI ĐĂNG KÝ** | Chọn MSSV/STT để sửa tên hoặc chụp lại mặt |
| **`9`** | **XÓA NGƯỜI ĐÃ ĐĂNG KÝ** | Chọn MSSV/STT để xóa khỏi hệ thống |
| **`Q`** | Thoát chương trình | |

> 🚀 **Chạy thẳng chức năng không cần qua Menu:**
> ```bash
> python main.py --stage 5    # Vào thẳng Đăng ký khuôn mặt mới
> python main.py --stage 6    # Vào thẳng Điểm danh tự động
> python main.py --stage 7    # Vào thẳng Xem lịch sử điểm danh
> ```

---

## 📁 Nơi lưu trữ dữ liệu

* **Danh sách sinh viên:** `data/students.csv`
* **Lịch sử điểm danh:** `data/attendance.csv`
* **Ảnh mẫu khuôn mặt:** `dataset/known_faces/{MSSV}/`
* **Model nhận diện:** `data/face_model.yml`

*(Toàn bộ dữ liệu này được lưu vĩnh viễn, lần sau mở lên hệ thống tự nhận diện lại bình thường, không cần đăng ký lại).*

---

## 🛠️ Xử lý lỗi thường gặp (FAQ)

1. **Lỗi `can't open file 'main.py': No such file or directory`:**
   - Bạn chưa vào đúng thư mục chứa code. Hãy kiểm tra lại lệnh `cd <duong_dan_den_thu_muc_A2_NDKM>`.
2. **Lỗi `ModuleNotFoundError: No module named 'cv2'`:**
   - Chưa kích hoạt môi trường ảo `.venv` hoặc chưa chạy `pip install -r requirements.txt`.
3. **Camera không mở được hoặc màn hình đen:**
   - Đảm bảo tắt Zoom, Google Meet, Teams, FaceTime trước khi chạy.
   - **macOS:** Vào `System Settings` ➜ `Privacy & Security` ➜ `Camera` ➜ Bật quyền cho Terminal / VS Code.
   - **Windows:** Vào `Settings` ➜ `Privacy & Security` ➜ `Camera` ➜ Bật *"Let desktop apps access your camera"*.
4. **Nhận diện báo `Unknown` dù đã đăng ký:**
   - Đứng ở nơi đủ ánh sáng, nhìn thẳng vào camera.
   - Đảm bảo bạn đã chạy lệnh cài đặt: `pip install opencv-contrib-python`.
# Face-Attendance-System
