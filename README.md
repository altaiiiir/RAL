# Riot Auto Login

A beautiful, lightweight desktop application for managing and automating League of Legends account logins.

## Features

- 🎨 **Modern UI** - Frameless window with League of Legends theming
- ⚡ **Zero Latency** - Direct function calls for perfect automation timing
- 🔐 **Account Management** - Save, edit, and delete multiple accounts
- 🌍 **Multi-Region Support** - Works with all League regions
- 🖱️ **Auto Login** - Automated client login using image recognition
- 💾 **Secure Storage** - Encrypted local account storage

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd LeagueOn
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

**Primary method (recommended):**
```bash
python main.py
```

**Alternative method:**
```bash
python app_ctk.py
```

### Using the Application

1. **Add Account**: Fill in username, password, and select region, then click Save
2. **Select Account**: Use the dropdown to choose a saved account
3. **Login**: Click the Login button to automatically login to League client
4. **Manage**: Edit or delete accounts as needed

### Window Controls

- **Minimize (—)**: Minimizes window to taskbar
- **Close (×)**: Closes application completely
- **Drag**: Click and drag the top area to move the window

## Requirements

- Python 3.11+
- Windows (for pyautogui automation)
- League of Legends client

## Dependencies

- `customtkinter>=5.2.0` - Modern UI framework
- `pyautogui>=0.9.54` - Automation library
- `pillow>=10.0.0` - Image processing

## Building Executable

To create a standalone .exe file:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

## File Structure

- `main.py` - Main entry point
- `app_ctk.py` - CustomTkinter application
- `app.py` - Legacy pywebview version (deprecated)
- `controllers/` - Business logic
- `models/` - Data models
- `requirements.txt` - Python dependencies

## Notes

- The application uses image recognition to find login fields
- Make sure the Riot Client is visible when using auto-login
- Account data is stored locally in encrypted format
- The frameless window design provides a modern gaming aesthetic

## Troubleshooting

- **Window not appearing**: Check if positioned off-screen on multi-monitor setups
- **Auto-login not working**: Ensure Riot Client is open and login screen is visible
- **Dependencies issues**: Try reinstalling in a fresh virtual environment