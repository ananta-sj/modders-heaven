# 👼 Modder's Heaven
**A universal, secure, and frictionless mod installer for Windows.**

Modding games shouldn't feel like performing open-heart surgery on your hard drive. Modder's Heaven is a lightweight desktop utility built to take the anxiety out of manual game modding. 

Instead of manually shuffling files and hoping you don't break your game, Modder's Heaven automatically finds the right files in a messy `.zip`, scans them locally for malware, seamlessly injects them into your game directory, and creates a secure backup. If a mod breaks your game? Click "Uninstall" to instantly roll back to your pristine, vanilla files.

### 🚀 Core Features
*   **Smart Payload Detection:** Automatically bypasses nested folders in poorly-packed zip files to find the actual mod data.
*   **Zero-Network Threat Scanning:** Hooks directly into Microsoft Defender (`MpCmdRun.exe`) to scan extracted payloads locally. No data leaves your machine.
*   **Foolproof Rollbacks:** Automatically backs up vanilla files before overwriting them and generates a JSON manifest for perfectly clean, one-click uninstalls.
*   **Standalone Executable:** Written in Python and packaged as a single `.exe` with a sleek, dark-mode CustomTkinter interface.


## Installation (For Users)
1. Download the latest `Modders Heaven.exe` from the [Releases](https://github.com/ananta-sj/modders-heaven/releases/) page.
2. Run the application (no installation required).

## Development Setup
To run the source code locally:
```bash
git clone [https://github.com/ananta-sj/modders-heaven.git](https://github.com/ananta-sj/modders-heaven.git)
cd modders-heaven
pip install -r requirements.txt
python app.py
