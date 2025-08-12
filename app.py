import os
import sys
import webview
from controllers.login_controller import RiotLoginController

class RiotAutoLoginAPI:
    def __init__(self):
        self.controller = RiotLoginController()
        self.window = None
    
    def set_window(self, window):
        self.window = window
    
    def get_accounts(self):
        """Get all accounts for the UI"""
        try:
            accounts = self.controller.get_accounts()
            print(f"API: returning {len(accounts)} accounts")
            return accounts
        except Exception as e:
            print(f"Error getting accounts: {str(e)}")
            return []
    
    def get_regions(self):
        """Get list of available regions"""
        try:
            regions = self.controller.get_regions()
            print(f"API: returning {len(regions)} regions")
            return regions
        except Exception as e:
            print(f"Error getting regions: {str(e)}")
            return []
    
    def save_account(self, username, password, region):
        """Save or update an account"""
        try:
            print(f"API: saving account {username} with region {region}")
            return self.controller.save_account(username, password, region)
        except Exception as e:
            print(f"Error saving account: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def delete_account(self, username):
        """Delete an account"""
        try:
            print(f"API: deleting account {username}")
            return self.controller.delete_account(username)
        except Exception as e:
            print(f"Error deleting account: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def login_to_client(self, username):
        """Login to League client using selected account"""
        try:
            print(f"API: logging in account {username}")
            return self.controller.login_to_client(username)
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def minimize_window(self):
        """Minimize the window"""
        try:
            if self.window:
                print("Minimizing window...")
                self.window.minimize()
                return {"success": True}
            return {"success": False, "message": "Window not available"}
        except Exception as e:
            print(f"Error minimizing window: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def close_window(self):
        """Close the window"""
        try:
            if self.window:
                print("Closing window...")
                self.window.destroy()
                return {"success": True}
            return {"success": False, "message": "Window not available"}
        except Exception as e:
            print(f"Error closing window: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def main():
    # Create API instance
    api = RiotAutoLoginAPI()
    
    # Set debugging options
    debug = True
    
    # Get the HTML file path - using the direct file:// protocol
    html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'web', 'templates', 'index.html'))
    url = f'file:///{html_path.replace(os.sep, "/")}'
    
    print(f"Loading HTML from: {url}")
    
    # Create window
    window = webview.create_window(
        title='Riot Auto Login',
        url=url,
        js_api=api,
        width=600,
        height=800,
        resizable=False,
        frameless=True,
        easy_drag=True,
        draggable=True
    )
    
    # Set window reference in API
    api.set_window(window)
    
    def on_bridge(window):
        # Fire the onbridge function which indicates pywebview is ready
        window.evaluate_js("if(window.onbridge){window.onbridge();}")
    
    # Start the app
    webview.start(on_bridge, window, debug=debug)


if __name__ == '__main__':
    main() 