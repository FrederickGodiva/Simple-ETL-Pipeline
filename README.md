<h1 align="center">Simple ETL Pipeline</h1>

---

# Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Usage](#usage)

# Overview

This project is a simple ETL (Extract, Transform, Load) pipeline built with Python. It demonstrates how to extract data from a website, transform it, and load it into a database. The pipeline is modular, and structured to be easily extensible for future data workflows.

# Project Structure

```tree
├── fashion_products.csv    # scraped dataset
├── main.py                 # entry point that runs the ETL pipeline
├── requirements.txt        # dependencies used in the project
├── tests                   # unit tests directory for each ETL component
|  ├── test_extract.py
|  ├── test_load.py
|  ├── test_transform.py
|  ├── __init__.py
|  └── __pycache__
└── utils                   # core ETL modules directory
   ├── extract.py
   ├── load.py
   ├── transform.py
   └── __pycache__
```

# Tech Stack

<a href="https://www.python.org/"><img src="https://go-skill-icons.vercel.app/api/icons?i=python" /></a>
<a href="https://www.sqlalchemy.org/"><img src="https://go-skill-icons.vercel.app/api/icons?i=sqlalchemy" /></a>
<a href="https://pandas.pydata.org/"><img src="https://go-skill-icons.vercel.app/api/icons?i=pandas" /></a>
<a href="https://docs.pytest.org/en/stable/"><img src="https://go-skill-icons.vercel.app/api/icons?i=pytest" /></a>
<a href="https://www.jetbrains.com/pycharm/"><img src="https://go-skill-icons.vercel.app/api/icons?i=pycharm" /></a>

# Usage
1. Clone this repository

   ```bash
   git clone https://github.com/FrederickGodiva/Simple-ETL-Pipeline.git
   ```

2. Install the Python virtual environment library
   
   Linux / Mac:
   ```bash
   sudo apt install python3-virtualenv
   ```

   Windows:
   ```bash
   pip install virtualenv
   ```

3. Create a Python virtual environment

   Linux / Mac:
   ```bash
   python3 -m virtualenv venv
   ```

   Windows:
   ```bash
   python -m virtualenv venv
   ```

4. Activate the virtual environment

   Linux / Mac:
   ```bash
   source venv/bin/activate
   ```

   Windows:
   ```bash
   venv/Scripts/activate
   ```

5. Install all the required dependencies

   ```bash
   pip install -r requirements.txt
   ```

6. Run the ETL pipeline

   Linux / Mac:
   ```bash
   python3 main.py
   ```

   Windows:
    ```bash
    python main.py
    ```

7. Run the unit tests

   Linux / Mac:
   ```bash
   python3 -m pytest tests
   ```
  
   Windows:
   ```bash
   python -m pytest tests
   ```
   
8. Run the test coverage report

    ```bash
    pytest --cov=utils --cov-report=html tests/
    ``` 

9. Exit the virtual environment

   ```bash
   deactivate
   ```
