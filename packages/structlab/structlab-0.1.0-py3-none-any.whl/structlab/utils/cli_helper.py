def cli_help():
    """Displays help information for structlab."""
    help_text = """
    structlab - Project Structure Generator

    Usage:
      structlab init [project_name]   Initialize a new project structure.
      structlab freeze                Save the current directory structure to layout.txt.
      structlab help                   Show this help message.

    Options:
      project_name  (Optional) Specify a project folder name. If not provided, it initializes in the current directory.
    
    Example:
      structlab init my_project       # Creates 'my_project' with the structure
      structlab freeze                # Saves the current folder structure
      structlab help                  # Shows this help menu
    """
    print(help_text.strip())
