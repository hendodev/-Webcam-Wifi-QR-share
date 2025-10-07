import re
import subprocess
import cv2
from pyzbar import pyzbar
import colorama
from colorama import Fore, Style
import platform
import os

def parse_wifi(qr):
    if not qr.startswith("WIFI:"):
        return None
    body = qr[len("WIFI:"):].rstrip(";")
    pairs = re.findall(r'([A-Z]):([^;]*)', body)
    data = {k: v for k, v in pairs}
    return {
        "ssid": data.get("S", ""),
        "type": data.get("T", ""),
        "password": data.get("P", ""),
        "hidden": data.get("H", "").lower() == "true"
    }

def connect_wifi(info):
    ssid = info["ssid"]
    password = info["password"]
    auth_type = info["type"].lower()
    system = platform.system()
    print(f"{Fore.GREEN}[+] Detected operating system: {system}{Style.RESET_ALL}")

    if system == "Windows":
        if auth_type == "nopass" or not password:
            cmd = ['netsh', 'wlan', 'connect', f'name={ssid}']
        else:
            profile = f"""
            <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
                <name>{ssid}</name>
                <SSIDConfig>
                    <SSID>
                        <name>{ssid}</name>
                    </SSID>
                </SSIDConfig>
                <connectionType>ESS</connectionType>
                <connectionMode>manual</connectionMode>
                <MSM>
                    <security>
                        <authEncryption>
                            <authentication>WPA2PSK</authentication>
                            <encryption>AES</encryption>
                            <useOneX>false</useOneX>
                        </authEncryption>
                        <sharedKey>
                            <keyType>passPhrase</keyType>
                            <protected>false</protected>
                            <keyMaterial>{password}</keyMaterial>
                        </sharedKey>
                    </security>
                </MSM>
            </WLANProfile>
            """.strip()

            with open("wifiprofile.xml", "w") as file:
                file.write(profile)

            subprocess.run(['netsh', 'wlan', 'add', 'profile', 'filename=wifiprofile.xml'], check=True)
            cmd = ['netsh', 'wlan', 'connect', f'name={ssid}']

        print(f"{Fore.GREEN}[+] Running: {' '.join(cmd)}{Style.RESET_ALL}")
        result = subprocess.run(cmd)
        os.remove("wifiprofile.xml") if os.path.exists("wifiprofile.xml") else None
        return result.returncode == 0

    elif system == "Linux":
        cmd = ['nmcli', 'dev', 'wifi', 'connect', ssid]
        if auth_type != "nopass" and password:
            cmd.extend(['password', password])
        print(f"{Fore.GREEN}[+] Running: {' '.join(cmd)}{Style.RESET_ALL}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"{Fore.GREEN}[+] {result.stdout}{Style.RESET_ALL}")
        return result.returncode == 0

    elif system == "Darwin":
        cmd = ['networksetup', '-setairportnetwork', 'en0', ssid]
        if auth_type != "nopass" and password:
            cmd.append(password)
        print(f"{Fore.GREEN}[+] Running: {' '.join(cmd)}{Style.RESET_ALL}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"{Fore.GREEN}[+] {result.stdout}{Style.RESET_ALL}")
        return result.returncode == 0

    return False

def main():
    colorama.init()
    print(f"{Fore.GREEN}[+] Detected operating system: {platform.system()}{Style.RESET_ALL}")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(f"{Fore.GREEN}[+] Cannot open webcam{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}[+] Scanning for QR. Press q to quit.{Style.RESET_ALL}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            qr_text = barcode.data.decode('utf-8')
            print(f"{Fore.GREEN}[+] Found: {qr_text}{Style.RESET_ALL}")
            info = parse_wifi(qr_text)
            if info:
                print(f"{Fore.GREEN}[+] Parsed: {info}{Style.RESET_ALL}")
                if connect_wifi(info):
                    print(f"{Fore.GREEN}[+] Connected successfully.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}[+] Connection failed.{Style.RESET_ALL}")
                cap.release()
                return

        cv2.imshow('QR scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

main()