# FPT Auto MAC Register & WiFi Switcher

Tool tự động hóa quy trình **register/change MAC Address** lên hệ thống của **Đại học FPT** và tự động chuyển đổi kết nối sang mạng **ĐH-FPT** sau khi đăng ký thành công.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey)

![preview] (utils/img/preview.png)

---

## 🚀 Tính năng chính

* **Auto Connect:**
  Tự động kết nối vào mạng đăng ký
  `FUHL-Register Your Laptop`
* **Auto Register:**
  Đăng nhập portal, lấy MAC máy và gửi yêu cầu đăng ký MAC
* **Auto Switch:**
  Tự động chuyển sang mạng **ĐH-FPT** sau khi đăng ký thành công
* **Lưu cấu hình:**
  Chỉ cần nhập MSSV & mật khẩu **một lần**
* **Bảo mật:**
  Mật khẩu được mã hóa và lưu local trong `config.json`

---

## 🛠 Cài đặt & Chạy từ Source Code

### 1️⃣ Yêu cầu

* Python **3.10+**
* Git (không bắt buộc)

### 2️⃣ Cài đặt thư viện

Mở Terminal (macOS) hoặc CMD / PowerShell (Windows) tại thư mục dự án:

```bash
pip install -r requirements.txt
```

### 3️⃣ Chạy tool

```bash
python main.py
```

---

## 📦 Run Built File (.exe / Unix Executable)

Nếu bạn tải file đã build sẵn (từ **Releases**):

### 🪟 Windows

1. Chuột phải vào `FPT_Wifi_Tool.exe`
2. Chọn **Run as Administrator**
3. Nhập **MSSV** và **Mật khẩu** (chỉ lần đầu)

---

### 🍎 macOS

Do cơ chế bảo mật của macOS, cần cấp quyền lần đầu:

```bash
xattr -cr FPT_Wifi_Tool
chmod +x FPT_Wifi_Tool
./FPT_Wifi_Tool
```

Nếu macOS hỏi quyền **Network / System Events**, chọn **Allow**.

---

## ⚙️ Cấu trúc dự án

```text
ChangeMACFPT/
│
├── main.py              # File chạy chính
├── requirements.txt     # Dependencies
├── config.json          # File config
│
├── core/
│   ├── __init__.py
│   └── register.py      # Logic đăng nhập & đăng ký MAC
│
└── utils/
    ├── __init__.py
    ├── crypto.py        # Mã hóa mật khẩu
    └── network.py       # Kết nối WiFi
```

---

## 🔨 Build file thủ công

Cài PyInstaller:

```bash
pip install pyinstaller
```

**Windows:**

```bash
pyinstaller --onefile --clean \
--name "FPT_Auto_Wifi" \
main.py
```

**macOS:**

```bash
pyinstaller --onefile --clean \
--name "FPT_Auto_Wifi" \
main.py
```

---

## Troubleshooting

-   **Lỗi "Unreachable network"**: Tool sẽ tự động thử lại 3 lần. Nếu vẫn lỗi, hãy kiểm tra lại Wi-Fi.
-   **Lỗi Location**: Cần được cấp quyền để tự động kết nối đến Wifi DH-FPT. Nếu không muốn cấp, có thể tự kết nối thủ công.
-   **Lỗi Admin**: Chạy với quyền quản trị "Run as Administrator".
-   **Không tìm thấy Profile**: Hãy kết nối thủ công vào mạng `DH-FPT` một lần để Windows lưu profile, sau đó chạy lại tool.
-   **Đổi tài khoản**: **xóa `config.json`** rồi chạy lại tool

---

## 🤝 Đóng góp

@imhuync

---

## 📌 Disclaimer

Tool được viết cho **mục đích học tập và hỗ trợ sinh viên** thao tác nhanh hơn.

Vui lòng sử dụng **đúng quy định của nhà trường**.

Config được lưu local trên máy của user, tool **không thu thập** bất kỳ thông tin nào.
