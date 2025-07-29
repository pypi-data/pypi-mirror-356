import os
from structlab.utils import detect_virtual_env, EXCLUDED_FOLDERS, print

def save_structure(output_file="layout.txt"):
    """Scans the current directory and saves the folder structure, excluding unwanted folders."""
    structure = ["├── ./"]  # Start with the root directory

    def capture_tree(directory=".", prefix=""):
        try:
            entries = sorted(os.listdir(directory))
        except PermissionError:
            print(f"Permission denied: {directory}", category="error")
            return
        
        # Exclude unwanted folders, including `.egg-info`
        entries = [
            e for e in entries 
            if e not in EXCLUDED_FOLDERS and 
            not detect_virtual_env(os.path.join(directory, e)) and
            not e.endswith(".egg-info")  # Ignore .egg-info directories
        ]

        files = [e for e in entries if os.path.isfile(os.path.join(directory, e))]
        folders = [e for e in entries if os.path.isdir(os.path.join(directory, e))]

        items = folders + files  # Directories first, then files

        for index, item in enumerate(items):
            path = os.path.join(directory, item)  # Define full path of item
            connector = "└── " if index == len(items) - 1 else "├── "
            structure.append(prefix + connector + item + ("/" if os.path.isdir(path) else ""))

            if os.path.isdir(path):  # Ensure it's a directory before recursive call
                new_prefix = prefix + ("    " if index == len(items) - 1 else "│   ")
                capture_tree(path, new_prefix)  # Call capture_tree with full path

    capture_tree(directory=".")  # Ensure directory is defined

    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(structure))

    print(f"Project layout saved to {output_file}", category="success")
