import os
import json
import getpass
import time
import subprocess
from utils.crypto import encode_pass, decode_pass
from utils.network import connect_register_wifi, switch_to_enterprise_wifi, disconnect_wifi, get_current_mac
from core.register import FPTRegister

CONFIG_FILE = "config.json"
REGISTER_WIFI = "FUHL-Register Your Laptop"
MAIN_WIFI = "DH-FPT"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_or_create_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data['username'], decode_pass(data['password'])
        except:
            pass
    
    print("\n--- CONFIG TÀI KHOẢN FPTU ---")
    u = input("Username (MSSV): ").strip()
    p = getpass.getpass("Password: ").strip()
    
    with open(CONFIG_FILE, "w") as f:
        json.dump({"username": u, "password": encode_pass(p)}, f)
    return u, p

def _check_and_open_location_settings():
    print("[Check] Đang kiểm tra quyền Location...")
    
    test = subprocess.run(
        ["netsh", "wlan", "show", "networks"], 
        capture_output=True, 
        text=True, 
        encoding="mbcs",
        errors="ignore"
    )
    output = (test.stdout + test.stderr).lower()
    if "location permission" in output or "quyền vị trí" in output:
        print("[WARN] Không tự động chuyển sang DH-FPT được vì chưa bật Location.")
        print("-> Đang mở cài đặt Location...")
        print("-> Hãy bật 'Location services' và 'Let desktop apps access your location'.")
        
        os.system("start ms-settings:privacy-location")
        
        input(">>> Sau khi bật xong, nhấn ENTER tại đây để tiếp tục...")
        return True
    return False

def main():
    clear_screen()

    print("===============================================")
    print(f"    AUTO CHANGE MAC ADDRESS FOR FPTU WIFI     ")
    print("===============================================")

    user, pwd = load_or_create_config()
    mac, clean_mac = get_current_mac()
    
    if not mac:
        print("Err: Không tìm thấy MAC Address!")
        return

    print(f"\n[1] Đang kết nối Wifi đăng ký: {REGISTER_WIFI}...")
    if connect_register_wifi(REGISTER_WIFI):
        print(f"-> Đã kết nối. Đang chạy tool đổi MAC...")
        reg = FPTRegister(user, pwd)
        success = False
        msg = ""
        
        for attempt in range(3):
            success, msg = reg.run(clean_mac)
            if success:
                break
            if "unreachable" in str(msg).lower() or "connection" in str(msg).lower():
                print(f"-> [!] Lỗi mạng ({attempt+1}/3). Đang thử lại sau 3s...")
                time.sleep(3)
            else:
                break
        print(f"-> Kết quả Server: {msg}")
        
        if success:
            print("-" * 47)
            print(f"[2] Đổi MAC Address thành công! Đang chuyển mạng sang '{MAIN_WIFI}'...")
            _check_and_open_location_settings()
            
            if switch_to_enterprise_wifi(MAIN_WIFI):
                print(f"[Info] Đã chuyển sang mạng '{MAIN_WIFI}'.")
            else:
                print(f"\n[Warn] Không thể tự động chuyển sang '{MAIN_WIFI}'.")
                print("       Hãy kết nối thủ công.")
        else:
            print(f"    -> Thất bại. Ngắt kết nối.")
            disconnect_wifi()
    else:
        print(f"\n[!] Không thể kết nối vào {REGISTER_WIFI}.")

    print("\nTool tự đóng sau 5s...")
    time.sleep(5)

if __name__ == "__main__":
    main()