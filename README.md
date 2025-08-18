# 🛰️ DroidProbe

**DroidProbe** is a lightweight command-line tool for probing Android devices over ADB (Android Debug Bridge) and gathering basic system information. It supports scanning single devices or batches via a list of IPs.

---

## 📋 Features

- Connects to Android devices over ADB (TCP/IP)
- Collects system metadata:
  - IP and MAC address
  - User privilege (`whoami`)
  - Device model and Android version
  - CPU architecture
  - Root detection (via `su` check)
- Outputs results in CSV format
- Works with single IPs or a list of targets

---

## 🚀 Usage

### 🔧 Requirements

- Python 3.7+
- ADB installed and in your system `$PATH`
- Python dependencies:
  ```bash
  pip install adbutils
  ```

---

### 📦 Run

```bash
python3 droidprobe.py -i 192.168.1.42
```

or

```bash
python3 droidprobe.py -f ip_list.txt
```

Where `ip_list.txt` contains one IP address per line.

---

## 🧪 Example Output

```csv
IPAddr,MACAddr,Whoami,Model,OSVer,CPUArch,su_present,rootable,scantime
192.168.1.42,dc4a3e223344,shell,Pixel 6,Android 12,arm64-v8a;armeabi-v7a,True,True,2025-08-18T15:45:00Z
```

---

## ⚠️ Notes

- Devices must be **listening on ADB over TCP (port 5555)**.
- The tool attempts to detect root access based on `whoami` and whether `su` can elevate privileges.
- MAC address resolution may vary by device or interface.

---
## 🛠️ Future Ideas

- Export to JSON or database
- Improved root detection
- Integration with mobile threat intelligence feeds

---

## 📄 License

MIT License — free to use, modify, and share.

