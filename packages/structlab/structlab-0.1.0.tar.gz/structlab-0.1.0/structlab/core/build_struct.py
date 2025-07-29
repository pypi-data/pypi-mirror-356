import os
from structlab.utils import print

DEFAULT_CONTENT = {
    "README.md": "# Project Title\n\nProject description here.",
    ".gitignore": "*.pyc\n__pycache__/\n.env\n",
}

def generate_from_layout(layout_file="layout.txt", output_dir="."):
    """Generates folders and files based on layout.txt, ensuring existing ones are skipped."""
    
    # Ensure target directory exists BEFORE doing anything
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(layout_file):
        print(f"Error: {layout_file} not found!", category="error")
        return

    with open(layout_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_path = []  

    for line in lines:
        line = line.rstrip()
        if not line or line == "├── ./":
            continue

        depth = (len(line) - len(line.lstrip(" │"))) // 4
        clean_name = line.replace("├──", "").replace("└──", "").replace("│", "").strip()

        current_path = current_path[:depth]  
        current_path.append(clean_name)  

        full_path = os.path.join(output_dir, *current_path)

        if clean_name.endswith("/"):  # If it's a folder
            if not os.path.exists(full_path):  # Skip if folder exists
                os.makedirs(full_path, exist_ok=True)
        else:  # If it's a file
            if not os.path.exists(full_path):  # Skip existing files
                os.makedirs(os.path.dirname(full_path), exist_ok=True)  
                with open(full_path, "w", encoding="utf-8") as f:
                    if clean_name in DEFAULT_CONTENT:
                        f.write(DEFAULT_CONTENT[clean_name])  # Only pre-fill known files
                    else:
                        f.write("")  # Create an empty file if unknown

    # Ensure README.md and .gitignore exist even if missing in layout.txt
    for file_name, content in DEFAULT_CONTENT.items():
        file_path = os.path.join(output_dir, file_name)
        if not os.path.exists(file_path):  # Skip if already exists
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

    print(f"Project structure initialized in: {os.path.abspath(output_dir)}", category="success")
