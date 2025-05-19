import os
import json
import sys

import pyautogui
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as tb
from tkinter import font
from app import main

ACCOUNTS_FILE = "accounts.json"
WINDOW_SIZE = (400, 450)

REGIONS = [
    "NA",
    "EUW",
    "EUNE",
    "PBE",
    "KR",
    "BR",
    "LAN",
    "LAS",
    "OCE",
    "TR",
    "RU",
    "JP",
    "PH",
    "SG",
    "TW",
    "VN",
    "TH",
    "HK",
    "CN",
    "SEA"
]


class LeagueAutoLoginApp:
    def __init__(self, root):
        self.root = root
        self.accounts = self.load_accounts()
        self.selected = tb.StringVar(value=self.get_display_name(self.accounts[0]) if self.accounts else "")
        self.region = tb.StringVar(value=self.accounts[0].get('region', REGIONS[0]) if self.accounts else REGIONS[0])
        self.setup_ui()

    def load_accounts(self):
        if not os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, "w") as f:
                json.dump([], f)
        with open(ACCOUNTS_FILE, "r") as f:
            accounts = json.load(f)
            # Ensure all accounts have a region field
            for acc in accounts:
                if 'region' not in acc:
                    acc['region'] = REGIONS[0]
            return accounts

    def save_accounts(self):
        with open(ACCOUNTS_FILE, "w") as f:
            json.dump(self.accounts, f, indent=2)

    def setup_ui(self):
        self.root.title("Riot Auto Login")
        self.root.resizable(False, False)
        self.center_window(*WINDOW_SIZE)

        self.canvas = tb.Canvas(self.root, width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])
        self.canvas.pack(fill="both", expand=True)

        self.set_background(resource_path("background.jpeg"))
        self.create_widgets()
        self.place_widgets()

    def center_window(self, width, height):
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x = int((sw / 2) - (width / 2))
        y = int((sh / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def set_background(self, image_path):
        bg_img = Image.open(image_path).resize(WINDOW_SIZE)
        self.bg_photo = ImageTk.PhotoImage(bg_img)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def create_widgets(self):
        custom_font = font.Font(family="Helvetica", size=11, weight="bold")
        self.title_label = tb.Label(self.root, text="League Auto Login", bootstyle="info", font=custom_font)

        self.account_menu = tb.Combobox(
            self.root, textvariable=self.selected,
            values=[self.get_display_name(acc) for acc in self.accounts], state="readonly", width=25
        )
        self.account_menu.bind("<<ComboboxSelected>>", self.on_account_select)

        self.login_button = tb.Button(self.root, text="Login", command=self.login)

        self.user_entry = tb.Entry(self.root)
        self.user_entry.insert(0, "Username")
        self.user_entry.bind("<FocusIn>", self.clear_placeholder)
        self.user_entry.bind("<FocusOut>", self.restore_placeholder)

        self.pass_entry = tb.Entry(self.root, show="*")
        self.pass_entry.insert(0, "Password")
        self.pass_entry.bind("<FocusIn>", self.clear_placeholder)
        self.pass_entry.bind("<FocusOut>", self.restore_placeholder)

        self.region_label = tb.Label(self.root, text="Region:", bootstyle="info")
        self.region_menu = tb.Combobox(
            self.root, textvariable=self.region,
            values=REGIONS, state="readonly"
        )

        self.save_button = tb.Button(self.root, text="Save", command=self.save_account)
        self.delete_button = tb.Button(self.root, text="Delete", bootstyle="danger", command=self.delete_account)

    def place_widgets(self):
        self.canvas.create_window(200, 40, window=self.title_label, width=180, height=30)
        self.canvas.create_window(200, 110, window=self.account_menu, width=140, height=30)
        self.canvas.create_window(200, 145, window=self.login_button, width=120, height=30)
        self.canvas.create_window(200, 190, window=self.user_entry, width=140, height=30)
        self.canvas.create_window(200, 225, window=self.pass_entry, width=140, height=30)
        self.canvas.create_window(140, 260, window=self.region_label, width=80, height=30)
        self.canvas.create_window(260, 260, window=self.region_menu, width=160, height=30)
        self.canvas.create_window(150, 330, window=self.save_button, width=80)
        self.canvas.create_window(250, 330, window=self.delete_button, width=80)

    def clear_placeholder(self, event):
        widget = event.widget
        if widget.get() in ("Username", "Password"):
            widget.delete(0, "end")

    def restore_placeholder(self, event):
        widget = event.widget
        if widget.get() == "":
            if widget == self.user_entry:
                widget.insert(0, "Username")
            elif widget == self.pass_entry:
                widget.insert(0, "Password")

    def on_account_select(self, event=None):
        display_name = self.selected.get()
        username = display_name.split(" (")[0] if " (" in display_name else display_name
        
        for acc in self.accounts:
            if acc['username'] == username:
                self.user_entry.delete(0, "end")
                self.pass_entry.delete(0, "end")
                self.user_entry.insert(0, acc['username'])
                self.pass_entry.insert(0, acc['password'])
                self.region.set(acc.get('region', REGIONS[0]))
                break

    def find_username_field(self):
        images = ["username_field.png", "username_field_alt.png"]
        for img in images:
            pos = pyautogui.locateCenterOnScreen(resource_path(img), confidence=0.7)
            if pos:
                return pos
        return None

    def login(self):
        acc = next((a for a in self.accounts if a['username'] == self.selected.get()), None)
        if not acc:
            messagebox.showerror("Error", "Account not found.")
            return

        self.root.withdraw()

        try:
            user_field = self.find_username_field()
            if not user_field:
                raise Exception("Username field not found.")

            pyautogui.click(user_field)
            pyautogui.write(acc['username'])
            pyautogui.press('tab')
            pyautogui.write(acc['password'])
            pyautogui.press('enter')

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            self.root.iconify()

    def save_account(self):
        new_user = self.user_entry.get().strip()
        new_pass = self.pass_entry.get().strip()
        new_region = self.region.get()

        if not new_user or not new_pass or not new_region:
            messagebox.showwarning("Missing Info", "Username, password, and region required.")
            return

        # Get currently selected account if any
        display_name = self.selected.get()
        selected_username = display_name.split(" (")[0] if " (" in display_name else display_name
        
        # Check if we're editing an existing account
        existing_account = None
        for i, acc in enumerate(self.accounts):
            if acc['username'] == selected_username:
                existing_account = i
                break
                
        # If editing selected account
        if existing_account is not None:
            # Update existing account
            self.accounts[existing_account] = {
                "username": new_user,
                "password": new_pass,
                "region": new_region
            }
            action = "updated"
        else:
            # Check if username already exists
            if any(acc['username'] == new_user for acc in self.accounts):
                messagebox.showwarning("Account Exists", "Account already exists.")
                return
                
            # Add new account
            self.accounts.append({
                "username": new_user,
                "password": new_pass,
                "region": new_region
            })
            action = "added"

        self.save_accounts()
        self.refresh_account_menu()
        messagebox.showinfo("Success", f"Account '{new_user}' {action}.")
        
        # Select the account we just saved
        for i, display in enumerate(self.account_menu['values']):
            if new_user in display:
                self.account_menu.current(i)
                self.on_account_select()
                break

    def delete_account(self):
        username = self.selected.get()
        self.accounts = [acc for acc in self.accounts if acc['username'] != username]
        self.save_accounts()
        self.refresh_account_menu()
        messagebox.showinfo("Deleted", f"Account '{username}' deleted.")

    def refresh_account_menu(self):
        display_names = [self.get_display_name(acc) for acc in self.accounts]
        self.account_menu['values'] = display_names
        self.selected.set(display_names[0] if display_names else "")
        self.user_entry.delete(0, "end")
        self.pass_entry.delete(0, "end")
        self.user_entry.insert(0, "Username")
        self.pass_entry.insert(0, "Password")
        self.region.set(REGIONS[0])

    def get_display_name(self, account):
        """Generate display name for account in format: username (REGION)"""
        return f"{account['username']} ({account.get('region', REGIONS[0])})"


def resource_path(filename):
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    if getattr(sys, 'frozen', False):  # running as bundled exe
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)


# ---- Run App ----
if __name__ == "__main__":
    main()
