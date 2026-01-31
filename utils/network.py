import platform
import time
import subprocess
import re
import sys
from getmac import get_mac_address

OS_NAME = platform.system()

if OS_NAME == "Windows":
    try:
        import pywifi
        from pywifi import const
    except ImportError:
        pass

def _win_get_connected_ssid():
    p = subprocess.run(
        ["netsh", "wlan", "show", "interfaces"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        shell=False
    )
    out = (p.stdout or "")
    m_ssid = re.search(r"^\s*SSID\s*:\s*(.+)\s*$", out, re.MULTILINE)
    m_state = re.search(r"^\s*State\s*:\s*(.+)\s*$", out, re.MULTILINE)
    ssid = m_ssid.group(1).strip() if m_ssid else ""
    state = m_state.group(1).strip().lower() if m_state else ""
    return ssid, state

def _win_wait_connected(ssid_name, timeout=25):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            check = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True,
                text=True,
                errors="ignore",
                shell=False
            )
            output = check.stdout.lower()
            ssid_lower = ssid_name.lower()
            
            is_connected = "connected" in output or "đã kết nối" in output
            
            if is_connected:
                if ssid_lower in output:
                    return True
                
                if "đh-fpt" in ssid_lower and "h-fpt" in output:
                    return True
        except:
            pass
        time.sleep(1)
    return False

def get_current_mac():
    try:
        mac = get_mac_address()
        if mac:
            return mac, mac.replace(":", "").replace("-", "").lower()
    except (OSError, Exception) as e:
        if OS_NAME == "Windows":
            try:
                result = subprocess.run(
                    ["netsh", "wlan", "show", "interfaces"],
                    capture_output=True,
                    text=True,
                    errors="ignore",
                    shell=False
                )
                output = result.stdout
                match = re.search(r"Physical address\s*:\s*([0-9A-Fa-f\-:]+)", output)
                if match:
                    mac = match.group(1).strip()
                    clean_mac = mac.replace(":", "").replace("-", "").lower()
                    return mac, clean_mac
            except:
                pass
    return None, None

def _connect_windows_open(ssid_name):
    wifi = pywifi.PyWiFi()
    try:
        iface = wifi.interfaces()[0]
    except:
        return False

    iface.disconnect()
    time.sleep(1)
    
    profiles = iface.network_profiles()
    for p in profiles:
        if p.ssid == ssid_name:
            iface.remove_network_profile(p)
            break
    
    profile = pywifi.Profile()
    profile.ssid = ssid_name
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_NONE)
    profile.cipher = const.CIPHER_TYPE_NONE
    
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    
    for _ in range(20):
        if iface.status() == const.IFACE_CONNECTED:
            time.sleep(5)
            return True
        time.sleep(1)
    return False

def _run_netsh(args):
    try:
        result = subprocess.run(
            ["netsh", "wlan"] + args,
            capture_output=True,
            text=True,
            encoding="mbcs", 
            errors="replace"
        )
        return result.stdout
    except Exception as e:
        print(f"[Error] Lỗi khi gọi netsh: {e}")
        return ""

def _connect_windows_enterprise(ssid_name):
    print(f"[Info] Đang kiểm tra profile: {ssid_name}...")
    
    profiles_out = _run_netsh(["show", "profiles"])
    
    available_profiles = []
    for line in profiles_out.split('\n'):
        if "All User Profile" in line:
            parts = line.split(":", 1)
            if len(parts) > 1:
                available_profiles.append(parts[1].strip())
    
    target_profile = None
    
    if ssid_name in available_profiles:
        target_profile = ssid_name
    else:
        for prof in available_profiles:
            if prof.lower() == ssid_name.lower():
                target_profile = prof
                break
    
    if not target_profile:
        print(f"[Warn] Không tìm thấy profile '{ssid_name}' trong máy.")
        return False

    print(f"[Info] Profile hợp lệ: '{target_profile}'. Đang kết nối...")

    _run_netsh(["disconnect"])
    time.sleep(1) 

    connect_out = _run_netsh(["connect", f"name={target_profile}"])

    out_lower = connect_out.lower()
    if "completed successfully" not in out_lower and "hoàn thành" not in out_lower:
        print(f"[Error] Kết nối thất bại: {connect_out.strip()}")
        return False
    return _win_wait_connected(target_profile, timeout=25)

def _connect_macos(ssid_name, is_enterprise=False):
    try:
        res = subprocess.run(['networksetup', '-listallhardwareports'], capture_output=True, text=True)
        match = re.search(r'Device: (en\d)', res.stdout)
        if not match: 
            return False
        device = match.group(1)

        if is_enterprise:
            subprocess.run(['networksetup', '-setairportpower', device, 'off'])
            time.sleep(2)
            subprocess.run(['networksetup', '-setairportpower', device, 'on'])
            return True
        else:
            cmd = ['networksetup', '-setairportnetwork', device, ssid_name]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            return proc.returncode == 0
    except:
        return False

def connect_register_wifi(ssid_name):
    if OS_NAME == "Windows":
        return _connect_windows_open(ssid_name)
    elif OS_NAME == "Darwin":
        return _connect_macos(ssid_name, is_enterprise=False)
    return False

def switch_to_enterprise_wifi(ssid_name):
    if OS_NAME == "Windows":
        return _connect_windows_enterprise(ssid_name)
    elif OS_NAME == "Darwin":
        return _connect_macos(ssid_name, is_enterprise=True)
    return False

def disconnect_wifi():
    try:
        if OS_NAME == "Windows":
            wifi = pywifi.PyWiFi()
            iface = wifi.interfaces()[0]
            iface.disconnect()
        elif OS_NAME == "Darwin":
            cmd_find = "networksetup -listallhardwareports | grep -A 1 Wi-Fi | tail -n 1 | awk '{print $2}'"
            dev = subprocess.check_output(cmd_find, shell=True).decode().strip()
            subprocess.run(['networksetup', '-setairportpower', dev, 'off'])
            time.sleep(1)
            subprocess.run(['networksetup', '-setairportpower', dev, 'on'])
    except:
        pass