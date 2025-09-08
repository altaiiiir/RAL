# Riot Auto Login (RAL)

Sick of having to always copy and paste to switch to your smurf accounts? RAL is a lightweight Open-Source tool for managing and automating Riot Client account logins with a single click of a button!

## ✨ Features

- 🔐 **Account Management** - Save, edit, and delete multiple accounts securely
- 🤖 **Auto Login** - Automated client login!
- 💾 **Local Storage** - JSON-based account storage with automatic persistence. No need to worry about your passwords being leaked, its all stored only on your computer!
- 🌍 **Multi-Region Support** - 20+ regions including NA, EUW, EUNE, KR, BR, and more
- 🎨 **Modern Frameless UI** - Qt-based interface with Riot theming and glass effects
- 🎯 **Zero Latency** - Direct function calls for perfect automation timing

## 🎥 Demo

https://github.com/user-attachments/assets/11e7eeed-5844-4295-962e-44615ad860b4

## 📥 Download Instructions

1. **Get the Latest Release**  
   - Go to the **Releases** section on the right-hand side of this GitHub page.  
   - Click on the **latest release**, then download `RAL.exe`.

2. **Browser Warning (Safe to Ignore)**  
   - Because this app is new and not widely downloaded, your browser may display a warning:  
     > *“RAL.exe isn’t commonly downloaded. Make sure you trust it before opening.”*  
   - If this appears, click the **3 dots** in the warning and select **Keep** to continue.

3. **Anti-Virus False Positive (Bypass Instructions)**  
   - Since the app is unsigned (I’m not paying for a code-signing certificate), some anti-virus programs may flag it as:  
     > *Trojan:Win32/Wacatac.B!ml*  
   - This is a **false positive**. The code is fully open-source—you can review it or scan it yourself.  
   - To run the app if your anti-virus blocks it:  
     - Open your anti-virus program.  
     - Find the **Quarantine** or **Blocked Threats** section.  
     - Locate `RAL.exe` and choose **Restore** or **Allow**.  
     - Add an **exception/allow rule** for `RAL.exe` so it doesn’t get flagged again.  
   - For more context, here’s a community discussion explaining this issue:  
     [Reddit: Can Wacatac be a false positive?](https://www.reddit.com/r/antivirus/comments/1g112hr/can_wacatac_be_false_positive/)

## 🚀 Local Run Setup

1. **Clone & Setup:**
   ```bash
   git clone https://github.com/altaiiiir/RAL.git
   cd RAL
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Run:**
   ```bash
   cd src
   python main.py
   ```

## 📱 Usage

1. **Add Account** - Enter username, password, and select region
2. **Select Account** - Choose from saved accounts dropdown
3. **Auto Login** - Click login to automatically authenticate with Riot Client
4. **Manage** - Edit or delete accounts as needed

## 🛠️ Requirements

- Python 3.11+
- Windows (for pyautogui automation)
- Riot Client installed

## 📦 Dependencies

- `PySide6` - Qt framework for modern UI
- `pyautogui` - Automation and image recognition

## 🏗️ Architecture

- **`src/`** - Main source code package
  - **`app.py`** - Application entry point and Qt application core with QML integration
  - **`controllers/`** - Business logic and automation
  - **`models/`** - Data models and account management
  - **`ui/`** - QML-based user interface
- **`assets/`** - Static assets (images, icons)
- **`resources/`** - Runtime-generated files

## 🔧 Build Executable

```bash
pip install pyinstaller
pyinstaller RAL.spec
```

## 📝 Notes

- Thanks for downloading! I hope it helps you switch between accounts a bit easier.
- If you have any suggestions or bugs, feel free to create an Issue on this Repo and I'll make sure to resolve them as soon as I can.
