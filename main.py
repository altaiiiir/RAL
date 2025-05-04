import os
import json
import time
import pyautogui
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as tb
from tkinter import font

ACCOUNTS_FILE = "accounts.json"
WINDOW_SIZE = (400, 400)


class LeagueAutoLoginApp:
    def __init__(self, root):
        self.root = root
        self.accounts = self.load_accounts()
        self.selected = tb.StringVar(value=self.accounts[0]['username'] if self.accounts else "")
        self.setup_ui()

    def load_accounts(self):
        if not os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, "w") as f:
                json.dump([], f)
        with open(ACCOUNTS_FILE, "r") as f:
            return json.load(f)

    def save_accounts(self):
        with open(ACCOUNTS_FILE, "w") as f:
            json.dump(self.accounts, f, indent=2)

    def setup_ui(self):
        self.root.title("League Auto Login")
        self.root.resizable(False, False)
        self.center_window(*WINDOW_SIZE)

        self.canvas = tb.Canvas(self.root, width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])
        self.canvas.pack(fill="both", expand=True)

        self.set_background("background.jpeg")
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
            values=[acc['username'] for acc in self.accounts], state="readonly"
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

        self.add_button = tb.Button(self.root, text="Save", command=self.add_account)
        self.edit_button = tb.Button(self.root, text="Edit", bootstyle="warning", command=self.edit_account)
        self.delete_button = tb.Button(self.root, text="Delete", bootstyle="danger", command=self.delete_account)

    def place_widgets(self):
        self.canvas.create_window(200, 40, window=self.title_label, width=180, height=30)
        self.canvas.create_window(200, 110, window=self.account_menu, width=140, height=30)
        self.canvas.create_window(200, 145, window=self.login_button, width=120, height=30)
        self.canvas.create_window(200, 190, window=self.user_entry, width=140, height=30)
        self.canvas.create_window(200, 225, window=self.pass_entry, width=140, height=30)
        self.canvas.create_window(100, 290, window=self.add_button, width=80)
        self.canvas.create_window(200, 290, window=self.edit_button, width=80)
        self.canvas.create_window(300, 290, window=self.delete_button, width=80)

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
        username = self.selected.get()
        for acc in self.accounts:
            if acc['username'] == username:
                self.user_entry.delete(0, "end")
                self.pass_entry.delete(0, "end")
                self.user_entry.insert(0, acc['username'])
                self.pass_entry.insert(0, acc['password'])
                break

    def login(self):
        acc = next((a for a in self.accounts if a['username'] == self.selected.get()), None)
        if not acc:
            messagebox.showerror("Error", "Account not found.")
            return

        self.root.withdraw()
        time.sleep(1)

        user_field = pyautogui.locateCenterOnScreen("username_field.png", confidence=0.8)
        if not user_field:
            messagebox.showerror("Error", "Username field not found.")
            return

        pyautogui.click(user_field)
        time.sleep(0.5)
        pyautogui.write(acc['username'])
        pyautogui.press('tab')
        pyautogui.write(acc['password'])
        pyautogui.press('enter')
        self.root.quit()

    def add_account(self):
        new_user = self.user_entry.get().strip()
        new_pass = self.pass_entry.get().strip()
        if not new_user or not new_pass:
            messagebox.showwarning("Missing Info", "Username and password required.")
            return

        self.accounts.append({"username": new_user, "password": new_pass})
        self.save_accounts()
        self.refresh_account_menu()
        messagebox.showinfo("Success", f"Account '{new_user}' added.")

    def edit_account(self):
        username = self.selected.get()
        new_user = self.user_entry.get().strip()
        new_pass = self.pass_entry.get().strip()

        if not new_user or not new_pass:
            messagebox.showwarning("Missing Info", "Username and password required.")
            return

        for acc in self.accounts:
            if acc['username'] == username:
                acc['username'] = new_user
                acc['password'] = new_pass
                break

        self.save_accounts()
        self.refresh_account_menu()
        messagebox.showinfo("Updated", f"Account '{username}' updated.")

    def delete_account(self):
        username = self.selected.get()
        self.accounts = [acc for acc in self.accounts if acc['username'] != username]
        self.save_accounts()
        self.refresh_account_menu()
        messagebox.showinfo("Deleted", f"Account '{username}' deleted.")

    def refresh_account_menu(self):
        names = [acc['username'] for acc in self.accounts]
        self.account_menu['values'] = names
        self.selected.set(names[0] if names else "")
        self.user_entry.delete(0, "end")
        self.pass_entry.delete(0, "end")
        self.user_entry.insert(0, "Username")
        self.pass_entry.insert(0, "Password")


# ---- Run App ----
if __name__ == "__main__":
    root = tb.Window(themename="pulse")
    app = LeagueAutoLoginApp(root)
    root.mainloop()
