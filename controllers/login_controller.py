import os
import sys
import pyautogui
from typing import Optional, Dict, List, Tuple, Any

from models.account import AccountManager, Account

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

class LeagueLoginController:
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
            user_field = self._find_username_field()
            if not user_field:
                return {"success": False, "message": "Username field not found"}
            
            pyautogui.click(user_field)
            pyautogui.write(account.username)
            pyautogui.press('tab')
            pyautogui.write(account.password)
            pyautogui.press('enter')
            
            return {"success": True, "message": f"Login attempted for '{username}'"}
        except Exception as e:
            return {"success": False, "message": f"Error during login: {str(e)}"}
    
    def _find_username_field(self) -> Optional[Tuple[int, int]]:
        """Find the username input field on screen"""
        images = ["username_field.png", "username_field_alt.png"]
        for img in images:
            pos = pyautogui.locateCenterOnScreen(self._resource_path(img), confidence=0.7)
            if pos:
                return pos
        return None
    
    def _resource_path(self, filename: str) -> str:
        """Get absolute path to resource, works for dev and for PyInstaller .exe"""
        if getattr(sys, 'frozen', False):  # running as bundled exe
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, filename) 