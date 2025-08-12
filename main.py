import os
import sys
from app import main

def resource_path(filename):
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    try:
        base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.abspath(".")
        return os.path.join(base_path, filename)
    except Exception:
        return os.path.join(os.path.abspath("."), filename)

# ---- Run App ----
if __name__ == "__main__":
    main()
