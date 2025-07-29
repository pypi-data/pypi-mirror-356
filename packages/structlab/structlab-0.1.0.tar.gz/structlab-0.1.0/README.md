<div align="center">
  <img src="./branding/logo/primary/structlab_logo.svg" alt="structlab Logo" width="170">
  <h1>structlab</h1>
  
  <p>
    <strong>A powerful CLI tool for generating and managing project folder structures.</strong>
  </p>

  <p>
  Structlab automates the creation of directories and files based on a predefined layout, 
  helping developers and teams maintain consistency across projects.  
  With commands for initialization, structure freezing, and usage guidance, it streamlines project setup and management.
  </p>
</div>

# Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Command List](#command-list)
- [Contributing](#contributing)
- [License](#license)

## Introduction

**Structlab** is a powerful and flexible CLI tool designed to automate the creation and management of project folder structures. It simplifies the process of setting up standardized directory layouts, ensuring consistency across multiple projects. The generated structure follows a modular design, separating CLI commands, core logic, and utility functions for maintainability and scalability. It is based on `layout.txt`, allowing users to define custom folder structures effortlessly.

With structlab, you can:

- Automatically generate project structures from predefined templates.
- Capture and save the structure of an existing project.
- Maintain organization and efficiency in project development.

Whether you're working on software development, research, or documentation projects, structlab provides a streamlined way to structure your files and directories.

## Features

- **Automated Project Structure Generation** – Quickly creates directories and files based on a predefined layout.
- **Structure Freezing** – Captures the current project structure and saves it for reuse.
- **Customizable Exclusions** – Allows specific files or directories to be ignored while scanning or generating structures.
- **Modular and Extensible** – Built with a utility-based architecture for easy expansion and customization.
- **Lightweight and Efficient** – Designed for speed and minimal dependencies.
- **Easy Installation and Usage** – Packaged for seamless integration with Python projects.

---

## Installation

### Prerequisites

Before installing structlab, ensure that you have the following dependencies installed:

- **Python 3.7 or later** – Required to run structlab
- **pip** – The Python package manager (comes pre-installed with Python)

### Installing via pip

You can install structlab globally using pip:

```sh
pip install structlab
```

To install it in a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install structlab
```

#### Installing from source

If you want to install the latest development version from source:

```sh
git clone https://github.com/anexlab/structlab.git
cd structlab
pip install .
```

#### Verifying the installation

After installation, you can verify that structlab is installed correctly by running:

```sh
structlab help
```

## Command List

structlab provides several commands to help manage and generate project structures. Below is a list of available commands:

| Command              | Description                                                                                                 | Usage                                         |
| -------------------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `init`               | Generates files and folders based on `layout.txt` in the current directory.                                 | `structlab init`                           |
| `init .`             | Explicitly generates files and folders in the current directory.                                            | `structlab init .`                         |
| `init <folder_name>` | Generates files and folders inside the specified folder.                                                    | `structlab init my_project`                |
| `freeze`             | Scans the current directory and saves its structure into `layout.txt`, excluding predefined system folders. | `structlab freeze`                         |
| `help`               | Displays usage instructions and available commands.                                                         | `structlab help`                           |
| `--version, -v`      | Displays the installed version of structlab.                                                             | `structlab --version` or `structlab -v` |

## Contributing

We appreciate contributions from the community! If you’d like to improve **structlab**, follow these steps:

#### 1. Fork & Clone the Repository

First, fork the repository on GitHub and then clone it to your local machine:

```sh
git clone https://github.com/anexlab/structlab.git
cd structlab
```

#### 2. Set Up a Virtual Environment (Optional)

To keep dependencies organized, set up a virtual environment:

```sh
# For Linux/macOS (bash/zsh)
python -m venv venv
source venv/bin/activate

# For Windows (CMD)
python -m venv venv
venv\Scripts\activate

# For Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

Then, install dependencies:

```sh
pip install -r requirements.txt
```

#### 3. Create a Feature Branch

Create a new branch for your changes:

```sh
git checkout -b feature-branch
```

#### 4. Make Your Changes

Implement your feature or fix issues and commit your changes:

```sh
git add .
git commit -m "feat: add new feature or fix issue"
```

#### 5. Run tests

Ensure all functionality works correctly before submitting changes:

```sh
pytest
```

#### 6. Push Your Changes & Create a Pull Request

Push your changes to your fork and create a pull request:

```sh
git push origin feature-branch
```

Then, go to GitHub, navigate to the Pull Requests section, and submit your PR.

## Contribution Guidelines

- Follow the project's code style and structure.
- Write meaningful commit messages.
- Ensure new features are properly documented.
- All contributions must be reviewed before merging.

## License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this project under the terms of the license.  
See the `LICENSE` file for more details.
