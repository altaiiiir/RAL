import json
import os
import sys
from typing import List, Dict, Optional, Any

class Account:
    def __init__(self, username: str, password: str, region: str):
        self.username = username
        self.password = password
        self.region = region
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "username": self.username,
            "password": self.password,
            "region": self.region
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Account':
        return cls(
            username=data.get('username', ''),
            password=data.get('password', ''),
            region=data.get('region', 'NA')
        )


class AccountManager:
    def __init__(self, accounts_file: str = None):
        if accounts_file is None:
            # Use resource_path to get the correct path for both dev and PyInstaller
            accounts_file = self._resource_path("accounts.json")
        
        self.accounts_file = accounts_file
        self.accounts: List[Account] = []
        self.load_accounts()
    
    def load_accounts(self) -> None:
        """Load accounts from JSON file"""
        try:
            if not os.path.exists(self.accounts_file):
                # Create the directory if it doesn't exist
                os.makedirs(os.path.dirname(self.accounts_file), exist_ok=True)

                template_data = []
                
                if getattr(sys, 'frozen', False):
                    try:
                        template_path = os.path.join(sys._MEIPASS, 'accounts.json')
                        if os.path.exists(template_path):
                            with open(template_path, 'r') as f:
                                template_data =  json.load(f)
                    except Exception:
                        pass
                
                with open(self.accounts_file, "w") as f:
                    json.dump(template_data, f)
                self.accounts = []
            else:
                with open(self.accounts_file, "r") as f:
                    accounts_data = json.load(f)
                    self.accounts = [Account.from_dict(acc) for acc in accounts_data]
        except Exception as e:
            # If there's an error loading accounts, start with empty list
            self.accounts = []
            print(f"Warning: Could not load accounts from {self.accounts_file}: {e}")
    
    def save_accounts(self) -> None:
        """Save accounts to JSON file"""
        try:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(self.accounts_file), exist_ok=True)
            with open(self.accounts_file, "w") as f:
                accounts_data = [acc.to_dict() for acc in self.accounts]
                json.dump(accounts_data, f, indent=2)
        except Exception as e:
            print(f"Error saving accounts to {self.accounts_file}: {e}")
    
    def add_account(self, username: str, password: str, region: str) -> Dict[str, Any]:
        """Add a new account or update existing one"""
        # Check if account already exists
        existing_index = self._find_account_index(username)
        
        # Create new account object
        account = Account(username, password, region)
        
        if existing_index is not None:
            # Update existing account
            self.accounts[existing_index] = account
            is_update = True
        else:
            # Add new account
            self.accounts.append(account)
            is_update = False
        
        self.save_accounts()
        return {"success": True, "is_update": is_update}
    
    def delete_account(self, username: str) -> Dict[str, Any]:
        """Delete an account by username"""
        index = self._find_account_index(username)
        if index is not None:
            self.accounts.pop(index)
            self.save_accounts()
            return {"success": True}
        return {"success": False}
    
    def get_account(self, username: str) -> Optional[Account]:
        """Get account by username"""
        for account in self.accounts:
            if account.username == username:
                return account
        return None
    
    def get_all_accounts(self) -> List[Account]:
        """Get all accounts"""
        return self.accounts
    
    def _find_account_index(self, username: str) -> Optional[int]:
        """Find account index by username"""
        for i, account in enumerate(self.accounts):
            if account.username == username:
                return i
        return None
    
    def _resource_path(self, filename: str) -> str:
        """Get absolute path to resource, works for dev and for PyInstaller .exe"""
        if getattr(sys, 'frozen', False):
            # use AppData for storage for executable
            appdata_dir = os.path.join(os.environ.get('APPDATA', ''), 'RiotAutoLogin')
            os.makedirs(appdata_dir, exist_ok=True)
            return os.path.join(appdata_dir, filename)
        else:
            # use current directory for dev
            return os.path.join(os.path.abspath("."), filename) 