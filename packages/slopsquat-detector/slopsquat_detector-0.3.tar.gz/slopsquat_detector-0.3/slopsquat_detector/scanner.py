import re
import ast
import json
import sys
import importlib.util
from pathlib import Path

def extract_packages(file_path: str) -> list[str]:
    path = Path(file_path)
    if path.suffix == '.py':
        return extract_from_py_file(file_path)
    elif path.suffix == '.ipynb':
        return extract_from_ipynb(file_path)
    else:
        return extract_from_requirements(file_path)

def extract_from_requirements(file_path: str) -> list[str]:
    pattern = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_.-]*)')
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [match.group(1) for line in lines if (match := pattern.match(line))]

def extract_from_py_file(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    return _extract_from_ast(tree)

def extract_from_ipynb(file_path: str) -> list[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        notebook = json.load(file)

    code = ""
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            code += ''.join(cell.get('source', [])) + '\n'
    
    try:
        tree = ast.parse(code, filename=file_path)
    except SyntaxError:
        return []
    
    return _extract_from_ast(tree)

def _extract_from_ast(tree: ast.AST) -> list[str]:
    packages = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                packages.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                packages.add(node.module.split('.')[0])
    return [pkg for pkg in packages if not is_stdlib(pkg)]

def is_stdlib(module_name: str) -> bool:
    """Returns True if the module is part of the Python standard library."""
    if module_name in sys.builtin_module_names:
        return True
    spec = importlib.util.find_spec(module_name)
    if spec is None or not spec.origin:
        return False
    return "site-packages" not in spec.origin
