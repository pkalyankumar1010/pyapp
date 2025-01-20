# Ping Checker

Ping Checker is a Python-based application with a graphical user interface (GUI) built using `tkinter`. This tool allows users to check the latency of a given URL by continuously pinging it. The application also implements license validation to ensure only authorized users can access its functionality.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Files Used](#files-used)
- [License Management](#license-management)
- [Error Handling](#error-handling)
- [License](#license)
- [Contributions](#contributions)
- [Contact](#contact)

---

## Features

- **Ping URL**: Input a URL and check its latency in real-time.
- **License Validation**: Uses encrypted license files to manage access.
- **User-Friendly Interface**: Simple GUI for easy interaction.
- **Error Handling**: Handles invalid URLs, expired licenses, and other errors gracefully.

---

## Installation

Before running the application, ensure you have the following prerequisites:

- Python 3.6 or newer
- Required Python libraries:
  - `tkinter` (comes pre-installed with Python)
  - `cryptography`

To install the `cryptography` library, run the following command:

```bash
pip install cryptography
```

## Running the Application

- Clone or download the repository:

```bash
git clone https://github.com/your-repo/ping-checker.git
cd ping-checker
```

- Run the script:

```bash
python ping_checker.py

```

- If prompted, select a valid license file to continue.

## Files Used

- ping_checker.py: The main program script that handles the core functionality of the Ping Checker application.
- license_path.json: This file stores the path to the selected license file for future use.

## License Management

- This application requires a valid license file to operate. The license file is an encrypted file (.lic) containing an expiration date. The application validates the license by decrypting the contents with an embedded secret key.

## License Validation Process:

- On startup, the application checks for the presence of a valid license file.
- If no valid license is found, the user is prompted to select a license file.
- The application decrypts the license file using the embedded secret key.
- If the license is valid and not expired, the application will become fully functional. Otherwise, it will show an error message.

## Error Handling

- Invalid License: If the license file is invalid or expired, an error message will be displayed.
- Missing License: If no license is available, the user will be prompted to select one. The program will not proceed until a valid license is provided.
- Invalid URL: If the user enters an invalid URL, the application will display an error message asking for a valid URL.
