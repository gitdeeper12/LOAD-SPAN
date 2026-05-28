#!/usr/bin/env python
"""System check script for LOAD-SPAN."""

import sys
import importlib

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python 3.9+ required (found {version.major}.{version.minor})")
        return False

def check_dependencies():
    """Check required dependencies."""
    required = [
        'numpy', 'scipy', 'pandas', 'matplotlib',
        'sklearn', 'xgboost', 'streamlit', 'plotly'
    ]
    
    missing = []
    for package in required:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing.append(package)
    
    return len(missing) == 0

def main():
    print("LOAD-SPAN System Check")
    print("=" * 40)
    
    python_ok = check_python_version()
    deps_ok = check_dependencies()
    
    if python_ok and deps_ok:
        print("\n✅ All checks passed! LOAD-SPAN is ready.")
    else:
        print("\n❌ Some checks failed. Please install missing dependencies.")
        print("Run: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
