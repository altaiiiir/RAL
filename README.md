# League Auto Login

A modern desktop application to manage your League of Legends accounts and automate the login process.

## Features

- Modern HTML/CSS/JS interface using PyWebView
- Add, edit and delete League of Legends accounts
- Select from all available regions
- Secure local storage of account information
- Automated login to League client
- Clean and user-friendly interface

## Requirements

- Python 3.8+
- PyWebView
- PyAutoGUI
- Pillow (PIL)

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/LeagueAutoLogin.git
cd LeagueAutoLogin
```

2. Install requirements:
```
pip install -r requirements.txt
```

3. Run the application:
```
python app.py
```

## Building Executable

To build a standalone executable:

```
pip install pyinstaller
pyinstaller --onefile --windowed --name "LeagueAutoLogin" --icon=icon.ico app.py
```

## Project Structure

```
LeagueAutoLogin/
├── app.py                  # Main application entry point
├── models/                 # Data models
│   ├── __init__.py
│   └── account.py          # Account management
├── controllers/            # Business logic
│   ├── __init__.py
│   └── login_controller.py # Login functionality
├── web/                    # Web UI
│   ├── templates/          # HTML templates
│   │   └── index.html
│   └── static/             # Static assets
│       ├── css/
│       │   └── styles.css
│       ├── js/
│       │   └── app.js
│       └── images/
│           └── background.jpg
├── icon.ico                # Application icon
├── background.jpeg         # Background image
├── accounts.json           # Saved accounts
└── README.md
```

## Security

Account information is stored locally in a JSON file. Passwords are stored in plaintext, so be careful with this file if you're concerned about security.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- League of Legends is a registered trademark of Riot Games, Inc.
- This application is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. 