import os
import sys
import pyautogui
from typing import Optional, Dict, List, Tuple, Any

from models.account import AccountManager

# Define available regions
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

class RiotLoginController:
    def __init__(self):
        self.account_manager = AccountManager()
    
    def get_accounts(self) -> List[Dict[str, str]]:
        """Get all accounts as dictionaries for the UI"""
        return [account.to_dict() for account in self.account_manager.get_all_accounts()]
    
    def get_regions(self) -> List[str]:
        """Get list of available regions"""
        return REGIONS
    
    def save_account(self, username: str, password: str, region: str) -> Dict[str, Any]:
        """Save or update an account"""
        if not username or not password or not region:
            return {"success": False, "message": "Username, password, and region are required"}
        
        try:
            result = self.account_manager.add_account(username, password, region)
            if result["is_update"]:
                return {"success": True, "message": f"Account '{username}' updated successfully"}
            else:
                return {"success": True, "message": f"Account '{username}' saved successfully"}
        except Exception as e:
            return {"success": False, "message": f"Error saving account: {str(e)}"}
    
    def delete_account(self, username: str) -> Dict[str, Any]:
        """Delete an account"""
        try:
            result = self.account_manager.delete_account(username)
            if result["success"]:
                return {"success": True, "message": f"Account '{username}' deleted successfully"}
            else:
                return {"success": False, "message": f"Account '{username}' not found"}
        except Exception as e:
            return {"success": False, "message": f"Error deleting account: {str(e)}"}
    
    def login_to_client(self, username: str) -> Dict[str, Any]:
        """Login to League client using selected account"""
        account = self.account_manager.get_account(username)
        if not account:
            return {"success": False, "message": "Account not found"}
        
        try:
            print(f"Attempting to login with account: {username}")
            
            # Set pyautogui settings for reliability
            pyautogui.PAUSE = 0.5  # Half second pause between actions
            pyautogui.FAILSAFE = True
            
            user_field = self._find_username_field()
            if not user_field:
                return {"success": False, "message": "Could not locate username field. Make sure Riot Client is open and visible."}
            
            print(f"Clicking username field at: {user_field}")
            
            # Clear any existing text first
            pyautogui.click(user_field)
            pyautogui.hotkey('ctrl', 'a')  # Select all
            pyautogui.press('delete')  # Clear field
            
            # Enter username
            pyautogui.write(account.username, interval=0.1)
            
            # Move to password field
            pyautogui.press('tab')
            
            # Clear password field and enter password
            pyautogui.hotkey('ctrl', 'a')  # Select all in password field
            pyautogui.write(account.password, interval=0.1)
            
            # Submit the form
            pyautogui.press('enter')
            
            return {"success": True, "message": f"Login attempted for '{username}'. If unsuccessful, ensure Riot Client is open and try positioning your cursor manually."}
            
        except Exception as e:
            error_msg = f"Error during login automation: {str(e)}"
            print(error_msg)
            return {"success": False, "message": error_msg}
    
    def _find_username_field(self) -> Optional[Tuple[int, int]]:
        """Find the username input field on screen"""
        images = ["username_field.png", "username_field_alt.png"]
        
        # Disable pyautogui's fail-safe to prevent interference
        pyautogui.FAILSAFE = False
        
        try:
            for img in images:
                try:
                    img_path = self._resource_path(img)
                    if not os.path.exists(img_path):
                        print(f"Warning: Image file not found: {img_path}")
                        continue
                    
                    # Try to locate the image with error handling
                    pos = pyautogui.locateCenterOnScreen(img_path, confidence=0.7)
                    if pos:
                        print(f"Found username field using {img} at position: {pos}")
                        return pos
                except Exception as e:
                    print(f"Error locating image {img}: {str(e)}")
                    continue
            
            # If image detection fails, return a default position (center of screen)
            # This is a fallback - users will need to manually position their cursor
            screen_width, screen_height = pyautogui.size()
            fallback_pos = (screen_width // 2, screen_height // 2)
            print(f"Image detection failed, using fallback position: {fallback_pos}")
            return fallback_pos
            
        except Exception as e:
            print(f"Critical error in _find_username_field: {str(e)}")
            return None
        finally:
            # Re-enable fail-safe
            pyautogui.FAILSAFE = True
    
    def _resource_path(self, filename: str) -> str:
        """Get absolute path to resource, works for dev and for PyInstaller .exe"""
        if getattr(sys, 'frozen', False):  # running as bundled exe
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, filename) 