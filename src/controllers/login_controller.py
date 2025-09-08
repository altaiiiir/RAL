import os
import sys
import pyautogui
from typing import Optional, Dict, List, Tuple, Any
from models.account import AccountManager
import pygetwindow as gw

class RiotLoginController:
    def __init__(self):
        self.account_manager = AccountManager()
    
    def get_accounts(self) -> List[Dict[str, str]]:
        return [account.to_dict() for account in self.account_manager.get_all_accounts()]
    
    def get_regions(self) -> List[str]:
        return ["NA", "KR", "CN", "PBE", "EUW", "EUNE", "VN", "BR", "TR", "LAN", "LAS", "RU", "OCE", "JP", "PH", "SG", "TW", "VN", "TH", "HK"]
    
    def get_speed_setting(self) -> int:
        """Get the current speed setting"""
        return self.account_manager.get_speed_setting()
    
    def set_speed_setting(self, speed: int) -> Dict[str, Any]:
        """Set the speed setting"""
        try:
            self.account_manager.set_speed_setting(speed)
            return {"success": True, "message": f"Speed setting updated to {['Slow', 'Default', 'Fast'][speed]}"}
        except Exception as e:
            return {"success": False, "message": f"Error saving speed setting: {str(e)}"}
    
    def save_account(self, username: str, password: str, region: str) -> Dict[str, Any]:
        if not username or not password or not region:
            return {"success": False, "message": "Username, password, and region are required"}
        
        try:
            result = self.account_manager.add_account(username, password, region)
            action = "updated" if result["is_update"] else "saved"
            return {"success": True, "message": f"Account '{username}' {action} successfully"}
        except Exception as e:
            return {"success": False, "message": f"Error saving account: {str(e)}"}
    
    def delete_account(self, username: str) -> Dict[str, Any]:
        try:
            result = self.account_manager.delete_account(username)
            if result["success"]:
                return {"success": True, "message": f"Account '{username}' deleted successfully"}
            return {"success": False, "message": f"Account '{username}' not found"}
        except Exception as e:
            return {"success": False, "message": f"Error deleting account: {str(e)}"}
    
    def login_to_client(self, username: str, speed: str = "Default") -> Dict[str, Any]:
        account = self.account_manager.get_account(username)
        if not account:
            return {"success": False, "message": "Account not found"}
        
        try:
            pyautogui.FAILSAFE = True
            
            # Set speed based on user selection
            speed_pauses = {"Fast": 0.01, "Default": 0.1, "Slow": 0.2}
            # Extract just the speed part (before the parentheses)
            clean_speed = speed.split(" (")[0] if " (" in speed else speed
            pyautogui.PAUSE = speed_pauses.get(clean_speed, 0.1)
            
            riot_window = self._find_riot_client_window()
            if not riot_window:
                return {"success": False, "message": "Could not locate Riot Client window. Make sure it's open and visible."}
            
            self._activate_riot_client_window()
            
            user_field = self._get_focus_position(riot_window)
            if not user_field:
                return {"success": False, "message": "Could not determine focus position."}
            
            # Fill username field
            pyautogui.click(user_field)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(account.username)
            
            # Fill password field
            pyautogui.press('tab')
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(account.password)
            
            # Tab 6 times and press enter
            for _ in range(6): pyautogui.press('tab')
            pyautogui.press('enter')
            
            # Click back on username field and press enter again
            pyautogui.click(user_field)
            pyautogui.press('enter')
            
            return {"success": True, "message": f"Login attempted for '{username}'. If unsuccessful, ensure Riot Client is open and try positioning your cursor manually."}
            
        except Exception as e:
            error_msg = f"Error during login automation: {str(e)}"
            return {"success": False, "message": error_msg}
    
    def _get_focus_position(self, riot_window: Tuple[int, int, int, int]) -> Optional[Tuple[int, int]]:
        try:
            username_x = riot_window[0] + 100
            username_y = riot_window[1] + 255
            return (username_x, username_y)
        except Exception as e:
            return None
    
    def _activate_riot_client_window(self) -> None:
        try:
            riot_windows = gw.getWindowsWithTitle("Riot Client")
            if riot_windows:
                win = riot_windows[0]
                win.activate()
                pyautogui.sleep(0.1)
            else:
                return None
        except Exception as e:
            return None
    
    def _find_riot_client_window(self) -> Optional[Tuple[int, int, int, int]]:
        try:
            riot_windows = gw.getWindowsWithTitle("Riot Client")
            
            if riot_windows:
                win = riot_windows[0]
                
                if hasattr(win, 'isMinimized') and win.isMinimized:
                    win.restore()
                    pyautogui.sleep(0.2)
                
                if hasattr(win, 'visible') and win.visible:
                    region = (win.left, win.top, win.width, win.height)
                    return region
                else:
                    return None
            else:
                return None
            
        except ImportError:
            return None
        except Exception as e:
            return None
    
    def _resource_path(self, filename: str) -> str:
        base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.abspath(".")
        return os.path.join(base_path, filename)
