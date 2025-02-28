# Get_Stats

## Prerequisites

Ensure you have the following tools installed:

- `python3`
- `pip3`
- `flask`
- `psutil`

## Installation

1. Update system packages:
    ```bash
    sudo apt update
    ```

2. Install Python 3:
    ```bash
    sudo apt install python3
    python3 --version
    ```

3. Install pip for Python 3:
    ```bash
    sudo apt install python3-pip
    pip3 --version
    ```

4. Install Python 3 virtual environment package:
    ```bash
    sudo apt install python3-venv
    ```

5. Create a virtual environment:
    ```bash
    python3 -m venv pythonenv
    ```

6. Activate the virtual environment:
    ```bash
    source pythonenv/bin/activate
    ```

7. Install required dependencies:
    ```bash
    pip install flask psutil
    ```

8. To deactivate the virtual environment:
    ```bash
    deactivate
    ```

9. Save the installed packages to a `requirements.txt` file:
    ```bash
    pip freeze > requirements.txt
    ```

10. Install dependencies from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To start the Python application:
```bash
python python_app.py
