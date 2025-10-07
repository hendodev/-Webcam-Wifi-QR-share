
# Webcam WiFi QR Share
Ever forget your WiFi password or just want a quick way to connect your laptop to your phone's hotspot? This Python script I made this script that lets you scan a WiFi QR code with your webcam and connect instantly. Works om (Windows/macOS/Linux/)

## What It Does

- Uses your webcam to scan WiFi QR codes.
- Grabs the WiFi details network (name/password).
- Connects your laptop to the WiFi network automatically.

## Stuff You Need
Before you start, make sure you have:

- Python 3.6+ and up.
- A working webcam.

## Extra Steps by OS

**Windows:** Install the Visual C++ Redistributable package from [here](https://www.techpowerup.com/download/visual-c-redistributable-runtime-package-all-in-one/).   
**Linux:**
`sudo apt-get install libzbar0`

**macOS:**
```
brew install zbar
```

## How to Set It Up

Clone this repo to your computer:

```bash
git clone https://github.com/hendodev/Webcam-Wifi-QR-share.git
cd Webcam-Wifi-QR-share
```

Install the required packages:

```bash
pip install -r requirements.txt
```

**Optional but recommended** Use a virtual environment [Linux]

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

## How to Use It

Run the script:

```bash
python wifiscan.py
```

It’ll:

* Show which OS you’re using (Windows/macOS/Linux).
* Access your webcam with a live feed.
* Wait for user to point it at a WiFi QR code.

Hold up a QR code to the webcam.

The script will read the QR code & connect to the WiFi then log the output

Press `q` to quit

## What It Looks Like

Here’s a sample of what you’ll see:

```
[+] Detected operating system: Windows
[+] Scanning for QR.
[+] Found: WIFI:S:MyNetwork;T:WPA2;P:MyPassword;;
[+] Parsed: {'ssid': 'MyNetwork', 'type': 'WPA2', 'password': 'MyPassword', 'hidden': False}
[+] Running: netsh wlan connect name=MyNetwork
[+] Connected successfully.
```

# Package install issues? Update pip first:

```bash
pip install --upgrade pip
```

Or install packages one by one:

```bash
pip install colorama opencv-python pyzbar
```
## License
This project is under the MIT License. Check the LICENSE file for details.

## Shoutouts
Big thanks to Quantum Sushi on Stack Overflow for the Windows WiFi profile.
[XML-FILE-NETSH](https://stackoverflow.com/questions/61757575/change-a-wifi-profiles-password-through-xml-file-and-netsh-wlan-or-python)
[Quantum Sushi Profile](https://stackoverflow.com/users/13211997/quantum-sushi)
