import os
import sys

def is_virtual_env():
    """Checks if the script is running inside a virtual environment."""
    return (hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

def detect_virtual_env(directory):
    """Detects if a specific folder is a Python virtual environment."""
    return (os.path.exists(os.path.join(directory, "bin", "activate")) or 
            os.path.exists(os.path.join(directory, "Scripts", "activate.bat")))
