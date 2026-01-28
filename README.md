# 📶 FPT Auto MAC Register & WiFi Switcher

Tool tự động hóa quy trình đăng ký địa chỉ MAC (MAC Address) lên hệ thống của Đại học FPT và tự động chuyển đổi kết nối sang mạng Enterprise (**ĐH-FPT**) sau khi đăng ký thành công. Hỗ trợ cả **Windows** và **macOS**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey)

## 🚀 Tính năng chính

* **Tự động nhận diện hệ điều hành** (Windows/macOS) để chọn phương thức kết nối phù hợp.
* **Auto Connect:** Tự động kết nối vào mạng đăng ký (`FUHL-Register Your Laptop`).
* **Auto Register:** Đăng nhập vào cổng thông tin, lấy MAC máy và gửi lệnh đổi MAC trên server.
* **Auto Switch:** Sau khi thành công, tự động chuyển mạng sang **ĐH-FPT** (Enterprise).
* **Lưu cấu hình:** Chỉ cần nhập MSSV và Mật khẩu một lần, lần sau tự động chạy.
* **Bảo mật:** Mật khẩu được mã hóa Base64 đơn giản và lưu cục bộ tại `config.json`.

---

## 🛠 Cài đặt & Chạy từ Source Code

### 1. Yêu cầu
* Python 3.x đã được cài đặt.
* Git (tùy chọn).

### 2. Cài đặt thư viện
Mở Terminal (macOS) hoặc CMD/PowerShell (Windows) tại thư mục dự án:

```bash
pip install -r requirements.txt
3. Chạy Tool
Bash
python main.py
📦 Hướng dẫn chạy file đóng gói (.exe / Unix Executable)
Nếu bạn tải file đã build sẵn (từ thư mục dist hoặc GitHub Actions), hãy làm theo hướng dẫn sau:

🪟 Windows
Chuột phải vào file FPT_Wifi_Tool.exe.

Chọn Run as Administrator (Bắt buộc để Tool có quyền điều khiển Card Wifi).

Nhập MSSV và Mật khẩu (lần đầu tiên).

🍎 macOS
Do cơ chế bảo mật của Apple, lần đầu chạy bạn cần cấp quyền:

Mở Terminal tại thư mục chứa file tool.

Chạy lệnh xóa thuộc tính kiểm dịch (Quarantine):

Bash
xattr -cr FPT_Wifi_Tool
Cấp quyền thực thi:

Bash
chmod +x FPT_Wifi_Tool
Chạy file. Nếu macOS hỏi quyền truy cập Network hoặc System Events, hãy chọn Allow.

⚙️ Cấu trúc dự án
Plaintext
FPT_Auto_Mac/
│
├── main.py              # File thực thi chính
├── requirements.txt     # Danh sách thư viện
├── config.json          # File cấu hình (Tự sinh ra khi chạy)
├── core/
│   ├── __init__.py
│   └── register.py      # Logic đăng nhập và gửi request đổi MAC
└── utils/
    ├── __init__.py
    ├── crypto.py        # Mã hóa password
    └── network.py       # Xử lý kết nối Wifi đa nền tảng (Win/Mac)
🔨 Cách đóng gói (Build)
Để tạo file chạy độc lập không cần cài Python:

Cách 1: Sử dụng GitHub Actions (Khuyên dùng)
Dự án đã hỗ trợ GitHub Actions. Chỉ cần push code lên GitHub, hệ thống sẽ tự động build ra file .exe (cho Windows) và file chạy cho macOS trong phần Actions > Artifacts.

Cách 2: Build thủ công trên máy
Cài đặt PyInstaller:

Bash
pip install pyinstaller
Windows:

Bash
pyinstaller --onefile --clean --name "FPT_Wifi_Tool" --hidden-import=pywifi --hidden-import=comtypes main.py
macOS:

Bash
pyinstaller --onefile --clean --name "FPT_Wifi_Tool" main.py
⚠️ Lưu ý quan trọng
Mạng Enterprise (ĐH-FPT):

Trên Windows: Tool sẽ gọi lệnh kết nối vào profile ĐH-FPT có sẵn. Nếu máy chưa từng kết nối, Windows sẽ hiện popup để bạn nhập User/Pass.

Trên macOS: Tool sẽ reset Wifi để máy tự ưu tiên vào mạng bảo mật cao hơn (ĐH-FPT).

File Config:

Nếu muốn đổi tài khoản, hãy xóa file config.json và chạy lại tool.

🤝 Đóng góp
Mọi ý kiến đóng góp hoặc báo lỗi vui lòng tạo Issue hoặc Pull Request trên GitHub.

Disclaimer: Tool được viết cho mục đích học tập và hỗ trợ sinh viên thao tác nhanh hơn. Sử dụng đúng quy định của nhà trường.
