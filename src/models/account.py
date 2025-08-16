import json
import os
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
            # Get the path to the resources directory (two levels up from src/models/)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            accounts_file = os.path.join(project_root, "resources", "accounts.json")
        
        self.accounts_file = accounts_file
        self.accounts: List[Account] = []
        self.load_accounts()
    
    def load_accounts(self) -> None:
        """Load accounts from JSON file"""
        if not os.path.exists(self.accounts_file):
            with open(self.accounts_file, "w") as f:
                json.dump([], f)
        
        with open(self.accounts_file, "r") as f:
            accounts_data = json.load(f)
            self.accounts = [Account.from_dict(acc) for acc in accounts_data]
    
    def save_accounts(self) -> None:
        """Save accounts to JSON file"""
        with open(self.accounts_file, "w") as f:
            accounts_data = [acc.to_dict() for acc in self.accounts]
            json.dump(accounts_data, f, indent=2)
    
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