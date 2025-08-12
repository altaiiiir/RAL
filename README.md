# Riot Auto Login

A lightweight desktop application to manage your Riot Games accounts and automate the login process.

## Features

- Modern frameless user interface using PyWebView
- Add, edit and delete Riot Games accounts
- Support for all Riot Games regions
- Secure local storage of account information
- One-click login to Riot Games clients
- Clean and minimal interface

## Requirements

- Python 3.8+
- Required libraries: pywebview, bottle, pyautogui

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/LeagueOn.git
cd LeagueOn
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python main.py
```

## Building Executable

To build a standalone executable:

```
pip install pyinstaller
pyinstaller RiotAutoLogin.spec
```

## Project Structure

```
LeagueOn/
├── main.py                 # Entry point
├── app.py                  # UI and server implementation
├── controllers/            # Business logic
│   └── login_controller.py # League login functionality
├── web/                    # Web UI
│   ├── templates/          # HTML templates
│   └── static/             # Static assets
│       ├── css/
│       ├── js/
│       └── images/
├── accounts.json           # Saved accounts data
└── README.md
```

## Security Note

Account information is stored locally in a JSON file. Please be aware that passwords are stored in plaintext, so ensure the security of this file.

## Disclaimer

This application is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games products. 