import argparse
import sys
from slopsquat_detector.scanner import extract_packages
from slopsquat_detector.validator import is_on_pypi

# Terminal colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def main():
    parser = argparse.ArgumentParser(description="Detect fake or hallucinated Python packages.")
    parser.add_argument("file", help="Path to requirements.txt, .py script, or .ipynb notebook")
    args = parser.parse_args()

    try:
        packages = extract_packages(args.file)
    except FileNotFoundError:
        print(f"{RED}Error: File '{args.file}' not found{RESET}")
        sys.exit(1)

    if not packages:
        print(f"{YELLOW}No packages found in {args.file}.{RESET}")
        sys.exit(0)

    print(f"\nScanning {len(packages)} dependencies...\n")
    
    missing = []
    for pkg in packages:
        if not is_on_pypi(pkg):
            print(f"{RED}[X] {pkg} not found on PyPI. Potential slopsquat!{RESET}")
            missing.append(pkg)
        else:
            print(f"{GREEN}[OK] {pkg} exists{RESET}")
    
    print(f"\n{len(missing)}/{len(packages)} packages missing from PyPI.")
    if missing:
        print(f"\n{YELLOW}Review these potentially unsafe packages:{RESET}")
        for pkg in missing:
            print(f"  - {pkg}")

if __name__ == "__main__":
    main()
