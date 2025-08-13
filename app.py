import os
import sys
import customtkinter as ctk
from tkinter import messagebox
import threading
from controllers.login_controller import RiotLoginController

# Set CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class RiotAutoLoginApp:
    def __init__(self):

        self.controller = RiotLoginController()
        self.accounts = []
        self.regions = []
        self.current_account = None
        self.restore_callback = None   # Track restore callback
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Riot Auto Login")
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        
        # League of Legends theme colors
        self.colors = {
            "primary": "#0A1428",
            "secondary": "#091428", 
            "accent": "#C89B3C",
            "text": "#F0E6D2",
            "danger": "#C34632",
            "success": "#1E8B55",
            "input_bg": "#0A1428",
            "card_bg": "#1a1a2e"
        }
        
        # Set window transparency for glassy effect
        self.root.attributes('-alpha', 0.96)
        
        # Configure window
        self.setup_window()
        self.create_widgets()
        self.load_data()
        
        # Setup background AFTER widgets are created
        self.setup_background()
        
    def setup_window(self):
        """Configure window properties"""
        # Get screen dimensions first
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Center window on screen properly
        x = (screen_width - 600) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"600x800+{x}+{y}")
        
        # Make window appear on top and focused
        self.root.lift()
        self.root.focus_force()
        self.root.attributes('-topmost', True)
        
        # Set window icon if available
        try:
            icon_path = self.resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
            
        # Make window frameless (no title bar) AFTER positioning
        self.root.overrideredirect(True)
        
        # Force window to appear and stay visible
        self.root.deiconify()
        self.root.lift()
        self.root.update()
        
        # Keep topmost briefly then remove
        self.root.after(2000, lambda: self.root.attributes('-topmost', False))
        
        # Add drag functionality
        self.setup_window_drag()
        
    def setup_background(self):
        """Setup background image if available"""
        try:
            import tkinter as tk
            from PIL import Image, ImageTk
            
            bg_path = self.resource_path("background.jpg")
            if os.path.exists(bg_path):
                # Load and resize background image
                bg_image = Image.open(bg_path)
                bg_image = bg_image.resize((600, 800), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(bg_image)
                
                # Create background label and ensure it's behind everything
                self.bg_label = tk.Label(self.root, image=self.bg_photo)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                
                # Force background to bottom layer
                self.bg_label.lower()
                
                # Also lower below the main frame specifically
                if hasattr(self, 'main_frame'):
                    self.bg_label.lower(self.main_frame)
                
                print("Background image loaded successfully")
            else:
                print("Background image not found, using default styling")
        except Exception as e:
            print(f"Could not load background image: {e}")
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container with padding - transparent to show background
        self.main_frame = ctk.CTkFrame(
            self.root, 
            fg_color="transparent",
            corner_radius=15
        )
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Custom drag bar
        self.create_drag_bar()
        
        # Header
        self.create_header()
        
        # Account selector section
        self.create_account_selector()
        
        # Account form section  
        self.create_account_form()
        
        # Notification area (initially hidden)
        self.create_notification_area()
        
    def create_header(self):
        """Create header with title"""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 30))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Riot Auto Login",
            font=ctk.CTkFont(family="Roboto", size=36, weight="bold"),
            text_color=self.colors["accent"]
        )
        title_label.pack()
        
    def create_drag_bar(self):
        """Create custom drag bar with window controls"""
        drag_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=30)
        drag_bar.pack(fill="x", pady=(0, 10))
        drag_bar.pack_propagate(False)
        
        # Window control buttons (right side)
        button_frame = ctk.CTkFrame(drag_bar, fg_color="transparent")
        button_frame.pack(side="right", padx=10)
        
        # Close button
        close_btn = ctk.CTkButton(
            button_frame,
            text="×",
            width=20,
            height=20,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=self.close_window
        )
        close_btn.pack(side="right", padx=(5, 0))
        
        # Minimize button  
        minimize_btn = ctk.CTkButton(
            button_frame,
            text="—",
            width=20,
            height=20,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#FFC107",
            hover_color="#FFB300",
            text_color="black",
            command=self.minimize_window
        )
        minimize_btn.pack(side="right", padx=(0, 5))
        
        # Make drag bar draggable
        self.drag_bar = drag_bar
        drag_bar.bind("<Button-1>", self.start_drag)
        drag_bar.bind("<B1-Motion>", self.on_drag)
        
    def setup_window_drag(self):
        """Setup window dragging functionality"""
        self.drag_start_x = 0
        self.drag_start_y = 0
        
    def start_drag(self, event):
        """Start dragging the window"""
        self.drag_start_x = event.x_root - self.root.winfo_x()
        self.drag_start_y = event.y_root - self.root.winfo_y()
        
    def on_drag(self, event):
        """Handle window dragging"""
        x = event.x_root - self.drag_start_x
        y = event.y_root - self.drag_start_y
        self.root.geometry(f"+{x}+{y}")
        
    def minimize_window(self):
        """Minimize the window properly"""
        # Temporarily enable title bar to allow proper minimize
        self.root.overrideredirect(False)
        # Minimize to taskbar normally
        self.root.iconify()
        
        # When window is restored, make it frameless again
        def check_restore():
            try:
                if self.root.state() == 'normal':
                    self.root.overrideredirect(True)
                    return
            except:
                pass
            # Check again in 100ms if still minimized
            self.restore_callback = self.root.after(100, check_restore)
        
        # Cancel any existing restore callback
        if self.restore_callback:
            self.root.after_cancel(self.restore_callback)
        
        # Start checking for restore and track the callback
        self.restore_callback = self.root.after(100, check_restore)
        
    def close_window(self):
        """Close the window and terminate application"""
        # Cancel any pending callbacks first
        try:
            if hasattr(self, 'restore_callback') and self.restore_callback:
                self.root.after_cancel(self.restore_callback)
        except:
            pass
            
        try:
            self.root.quit()      # Exit mainloop  
            self.root.destroy()   # Destroy window
        except:
            pass
        
        # Force terminate to ensure clean exit
        import sys
        sys.exit(0)
        
    def create_account_selector(self):
        """Create account selection section"""
        # Account selector frame - semi-transparent glassy effect
        selector_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color=("gray14", "gray8"),  # Semi-transparent dark
            corner_radius=12,
            border_width=1,
            border_color="#3C3C41"
        )
        selector_frame.pack(fill="x", pady=(0, 20), padx=20, ipady=20)
        
        # Account selection label
        select_label = ctk.CTkLabel(
            selector_frame,
            text="Select Account",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text"]
        )
        select_label.pack(pady=(0, 10))
        
        # Account dropdown
        self.account_var = ctk.StringVar(value="Select an account")
        self.account_dropdown = ctk.CTkComboBox(
            selector_frame,
            variable=self.account_var,
            values=["Select an account"],
            command=self.on_account_select,
            font=ctk.CTkFont(size=14),
            width=400,
            height=35
        )
        self.account_dropdown.pack(pady=(0, 15))
        
        # Login button
        self.login_btn = ctk.CTkButton(
            selector_frame,
            text="LOGIN",
            command=self.login_to_client,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors["accent"],
            hover_color="#D4AC4A",
            text_color=self.colors["primary"],
            width=400,
            height=40
        )
        self.login_btn.pack()
        
    def create_account_form(self):
        """Create account details form"""
        # Account form frame - semi-transparent glassy effect
        form_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color=("gray14", "gray8"),  # Semi-transparent dark
            corner_radius=12,
            border_width=1,
            border_color="#3C3C41"
        )
        form_frame.pack(fill="x", pady=(0, 20), padx=20, ipady=20)
        
        # Form title
        form_title = ctk.CTkLabel(
            form_frame,
            text="Account Details",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["accent"]
        )
        form_title.pack(pady=(0, 20))
        
        # Username field
        username_label = ctk.CTkLabel(
            form_frame,
            text="Username",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text"]
        )
        username_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter username",
            font=ctk.CTkFont(size=14),
            width=400,
            height=35
        )
        self.username_entry.pack(pady=(0, 15))
        self.username_entry.bind("<KeyRelease>", self.on_username_change)
        
        # Password field
        password_label = ctk.CTkLabel(
            form_frame,
            text="Password", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text"]
        )
        password_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter password",
            show="*",
            font=ctk.CTkFont(size=14),
            width=400,
            height=35
        )
        self.password_entry.pack(pady=(0, 15))
        
        # Region field
        region_label = ctk.CTkLabel(
            form_frame,
            text="Region",
            font=ctk.CTkFont(size=14, weight="bold"), 
            text_color=self.colors["text"]
        )
        region_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.region_var = ctk.StringVar()
        self.region_dropdown = ctk.CTkComboBox(
            form_frame,
            variable=self.region_var,
            values=[],
            font=ctk.CTkFont(size=14),
            width=400,
            height=35
        )
        self.region_dropdown.pack(pady=(0, 20))
        
        # Action buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20)
        
        self.save_btn = ctk.CTkButton(
            button_frame,
            text="SAVE",
            command=self.save_account,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["accent"],
            hover_color="#D4AC4A",
            text_color=self.colors["primary"],
            width=180,
            height=35
        )
        self.save_btn.pack(side="left", padx=(0, 10))
        
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="DELETE",
            command=self.delete_account,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["danger"],
            hover_color="#D44A42",
            width=180,
            height=35
        )
        self.delete_btn.pack(side="right")
        
    def create_notification_area(self):
        """Create notification area"""
        self.notification_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.notification_frame.pack(fill="x", pady=(10, 0))
        
        self.notification_label = ctk.CTkLabel(
            self.notification_frame,
            text="",
            font=ctk.CTkFont(size=14),
            fg_color=self.colors["success"],
            corner_radius=5,
            width=400,
            height=40
        )
        # Initially hidden
        
    def load_data(self):
        """Load accounts and regions from controller"""
        try:
            # Load accounts
            self.accounts = self.controller.get_accounts()
            self.update_account_dropdown()
            
            # Load regions - convert to format expected by dropdown
            region_codes = self.controller.get_regions()
            self.regions = [{"code": code, "name": code} for code in region_codes]
            self.update_region_dropdown()
            
        except Exception as e:
            self.show_notification(f"Error loading data: {str(e)}", "error")
            
    def update_account_dropdown(self):
        """Update account dropdown with current accounts"""
        if self.accounts:
            values = [f"{acc['username']} ({acc['region']})" for acc in self.accounts]
            self.account_dropdown.configure(values=["Select an account"] + values)
        else:
            self.account_dropdown.configure(values=["Select an account"])
            
    def update_region_dropdown(self):
        """Update region dropdown with available regions"""
        if self.regions:
            values = [region["code"] for region in self.regions]
            self.region_dropdown.configure(values=values)
            
    def on_account_select(self, value):
        """Handle account selection"""
        if value == "Select an account":
            self.clear_form()
            return
            
        # Extract username from the dropdown value
        username = value.split(" (")[0]
        self.current_account = next((acc for acc in self.accounts if acc["username"] == username), None)
        
        if self.current_account:
            # Fill form with account details
            self.username_entry.delete(0, "end")
            self.username_entry.insert(0, self.current_account["username"])
            
            self.password_entry.delete(0, "end") 
            self.password_entry.insert(0, self.current_account["password"])
            
            self.region_var.set(self.current_account["region"])
            
    def on_username_change(self, event):
        """Handle username field changes"""
        if self.account_var.get() != "Select an account":
            self.account_var.set("Select an account")
            self.current_account = None
            
    def clear_form(self):
        """Clear the form fields"""
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end") 
        self.region_var.set("")
        self.current_account = None
        
    def save_account(self):
        """Save account using controller"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        region = self.region_var.get()
        
        if not username or not password or not region:
            self.show_notification("Please fill in all fields", "error")
            return
            
        try:
            result = self.controller.save_account(username, password, region)
            if result["success"]:
                self.show_notification("Account saved successfully", "success")
                self.load_data()  # Reload accounts
                
                # Select the saved account
                self.root.after(100, lambda: self.account_var.set(f"{username} ({region})"))
            else:
                self.show_notification(f"Error saving account: {result['message']}", "error")
                
        except Exception as e:
            self.show_notification(f"Error saving account: {str(e)}", "error")
            
    def delete_account(self):
        """Delete account with confirmation"""
        if not self.current_account:
            self.show_notification("Please select an account to delete", "error")
            return
            
        # Show confirmation dialog
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the account '{self.current_account['username']}'?"
        )
        
        if result:
            try:
                delete_result = self.controller.delete_account(self.current_account["username"])
                if delete_result["success"]:
                    self.show_notification("Account deleted successfully", "success")
                    self.load_data()  # Reload accounts
                    self.clear_form()
                    self.account_var.set("Select an account")
                else:
                    self.show_notification(f"Error deleting account: {delete_result['message']}", "error")
                    
            except Exception as e:
                self.show_notification(f"Error deleting account: {str(e)}", "error")
                
    def login_to_client(self):
        """Login to client using controller"""
        selected_value = self.account_var.get()
        if selected_value == "Select an account":
            self.show_notification("Please select an account to login", "error")
            return
            
        # Extract username from dropdown value
        username = selected_value.split(" (")[0]
        
        self.show_notification("Logging in...", "info")
        
        # Run login in separate thread to prevent UI blocking
        def login_thread():
            try:
                result = self.controller.login_to_client(username)
                
                # Update UI from main thread
                self.root.after(0, lambda: self.handle_login_result(result))
                
            except Exception as e:
                self.root.after(0, lambda: self.show_notification(f"Login error: {str(e)}", "error"))
                
        threading.Thread(target=login_thread, daemon=True).start()
        
    def handle_login_result(self, result):
        """Handle login result on main thread"""
        if result["success"]:
            self.show_notification("Login successful!", "success")
        else:
            self.show_notification(f"Login failed: {result['message']}", "error")
            
    def show_notification(self, message, msg_type="info"):
        """Show notification message"""
        colors = {
            "success": self.colors["success"],
            "error": self.colors["danger"],
            "info": "#2196F3"
        }
        
        self.notification_label.configure(
            text=message,
            fg_color=colors.get(msg_type, colors["info"])
        )
        self.notification_label.pack(pady=10)
        
        # Auto-hide success/info messages after 5 seconds
        if msg_type in ["success", "info"]:
            self.root.after(5000, self.hide_notification)
            
    def hide_notification(self):
        """Hide notification message"""
        self.notification_label.pack_forget()
        
    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
        
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = RiotAutoLoginApp()
    app.run()


if __name__ == '__main__':
    main() 
