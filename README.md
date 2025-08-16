# Riot Auto Login (RAL)

A modern desktop application for managing and automating Riot Client account logins with a beautiful frameless UI.

## ✨ Features

- 🎨 **Modern Frameless UI** - Qt-based interface with Riot theming and glass effects
- 🔐 **Account Management** - Save, edit, and delete multiple accounts securely
- 🌍 **Multi-Region Support** - 20+ regions including NA, EUW, EUNE, KR, BR, and more
- 🤖 **Auto Login** - Automated client login using image recognition and pyautogui
- 💾 **Local Storage** - JSON-based account storage with automatic persistence
- 🖱️ **Smart Automation** - Intelligent field detection and reliable input simulation
- 🎯 **Zero Latency** - Direct function calls for perfect automation timing

## 🚀 Quick Start

1. **Clone & Setup:**
   ```bash
   git clone <repository-url>
   cd RAL
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Run:**
   ```bash
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
- `pillow` - Image processing support

## 🏗️ Architecture

- **`main.py`** - Application launcher
- **`src/`** - Main source code package
  - **`main.py`** - Application entry point
  - **`app.py`** - Qt application core with QML integration
  - **`controllers/`** - Business logic and automation
  - **`models/`** - Data models and account management
  - **`ui/`** - QML-based user interface
- **`assets/`** - Static assets (images, icons)
- **`resources/`** - Runtime-generated files

## 🔧 Build Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

## 📝 Notes

- Uses image recognition to locate login fields automatically
- Ensure Riot Client is visible when using auto-login
- Account data stored locally in JSON format
- Frameless design provides modern gaming aesthetic
- Supports all major League of Legends regions

## 🐛 Troubleshooting

- **Window not visible** - Check multi-monitor positioning
- **Auto-login fails** - Ensure Riot Client is open and login screen visible
- **Dependencies issues** - Use fresh virtual environment