import tempfile
import json
from pathlib import Path
from slopsquat_detector.scanner import extract_packages

def test_extract_packages_from_requirements():
    content = """
    valid-package==1.0.0
    _private_package>=0.2
    with.version<=2.1.3
    # Commented line
    """
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as f:
        f.write(content)
        f.seek(0)
        pkgs = extract_packages(f.name)
    assert pkgs == ["valid-package", "_private_package", "with.version"]

def test_extract_packages_from_py_file():
    code = """
    import os
    import numpy
    from sklearn.model_selection import train_test_split
    from . import local_module
    """
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as f:
        f.write(code)
        f.seek(0)
        pkgs = extract_packages(f.name)
    assert "numpy" in pkgs
    assert "sklearn" in pkgs
    assert "os" not in pkgs  
    assert "local_module" not in pkgs  

def test_extract_packages_from_ipynb():
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "source": [
                    "import pandas as pd\n",
                    "from matplotlib import pyplot as plt\n",
                    "import sys\n"
                ]
            },
            {
                "cell_type": "markdown",
                "source": ["This is a markdown cell."]
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5
    }
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.ipynb', delete=False, encoding='utf-8') as f:
        json.dump(notebook, f)
        f.seek(0)
        pkgs = extract_packages(f.name)
    assert "pandas" in pkgs
    assert "matplotlib" in pkgs
    assert "sys" not in pkgs 
