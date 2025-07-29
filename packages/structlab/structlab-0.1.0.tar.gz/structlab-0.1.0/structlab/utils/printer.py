import sys

# Define color codes
COLORS = {
    "error": "\033[91m",   # Red
    "success": "\033[92m", # Green
    "warning": "\033[93m", # Yellow
    "reset": "\033[0m"     # Reset to default
}

# Backup the original print function first
super_print = __builtins__.print if hasattr(__builtins__, "print") else sys.stdout.write

def print(*args, category=None, **kwargs):
    """Custom print function with colored output for error, success, and warning messages."""
    if category in COLORS:
        sys.stdout.write(COLORS[category])  # Set color
        super_print(*args, **kwargs)        # Call built-in print
        sys.stdout.write(COLORS["reset"] + "\n")  # Reset color with newline
    else:
        super_print(*args, **kwargs)        # Normal print




'''def print_error(message):
    """Prints error messages in red using the system's default terminal color."""
    print(f"\033[91m Error: {message}\033[0m", file=sys.stderr)'''