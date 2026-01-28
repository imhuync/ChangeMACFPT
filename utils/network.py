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

def get_current_mac():
    mac = get_mac_address()
    if mac:
        return mac, mac.replace(":", "").replace("-", "").lower()
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

def _connect_windows_enterprise(ssid_name):
    check_cmd = f'netsh wlan show profiles name="{ssid_name}"'
    check = subprocess.run(check_cmd, capture_output=True, text=True, shell=True)
    
    if "not found" in check.stdout or "is not found" in check.stdout:
        return True

    cmd = f'netsh wlan connect name="{ssid_name}"'
    subprocess.run(cmd, shell=True)
    return True

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