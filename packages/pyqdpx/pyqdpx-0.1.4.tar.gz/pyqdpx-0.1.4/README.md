# pyqdpx

A Python module to process Qualitative Data Exchange (QDPX) XML files, which are zip-compressed archives containing a `project.qde` XML file and a `Sources` directory.

## Features

* List source files within a `.qdpx` archive.
* Retrieve content of individual source files.
* Load and manipulate `project.qde` XML data.
* Manage users (add, list) within the project.
* Manage qualitative codes (add, modify, delete, navigate hierarchy).
* Save modifications back to the `.qdpx` archive, ensuring data integrity.

## Installation

You can install `pyqdpx` using pip:

```bash
pip install pyqdpx
```

If you want to install from source for development:

```bash
git clone https://github.com/DEPT-metagenom/pyqdpx.git
cd pyqdpx
pip install .
```

## Usage

Here's a quick example of how to use pyqdpx:

```python
from pyqdpx import QDPX, User, Code
import os

# Assume 'my_project.qdpx' exists and is a valid QDPX file
# For demonstration, you might create a dummy file first as in your tests.

# Initialize the QDPX object
qdpx_file = QDPX("my_project.qdpx")

# Get the QDE project
project = qdpx_file.get_project()

if project:
    print("Project Title:", project._bs4_obj.find('Title').string)

    # List users
    print("\nUsers:")
    for user_guid, user_obj in project.users.items():
        print(f"- {user_obj.name} (ID: {user_obj.id})")

    # Add a new user
    new_user = User(id="AL", name="Ada Lovelace")
    project.add_user(new_user)
    print(f"\nAdded new user: {new_user.name}")

    # Print code tree
    print("\nCode Tree:")
    project.print_code_tree()

    # Find and modify a code
    susceptibility_code = project.find_code("1. Perceived Susceptibility")
    if susceptibility_code:
        print(f"\nOriginal Susceptibility Description: {susceptibility_code.description}")
        susceptibility_code.description = "Updated description for perceived susceptibility."
        print(f"New Susceptibility Description: {susceptibility_code.description}")

    # Save changes (this will update the project.qde inside the zip)
    project.save()
    print("\nProject saved successfully!")
else:
    print("Could not load project.")

# Clean up (if you created a dummy file for testing)
# os.remove("my_project.qdpx")
```

## Running Tests

To run the unit tests, navigate to the root directory of the package (`pyqdpx_package/`) and use pytest:

```bash
pip install pytest
pytest
```

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.LicenseThis project is licensed under the MIT License - see the LICENSE file for details.
