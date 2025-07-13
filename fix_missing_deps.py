#!/usr/bin/env python3
"""
Quick fix for missing pydantic-settings dependency
"""

import subprocess
import sys

def install_package(package):
    """Install a package and handle errors"""
    print(f"📦 Installing {package}...")
    try:
        result = subprocess.run(
            f"python -m pip install {package}",
            shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {package} installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e.stderr}")
        return False

def main():
    print("🔧 Fixing Missing Dependencies")
    print("=" * 40)
    
    # Install the missing dependency
    missing_packages = [
        "pydantic-settings==2.1.0",
        "pydantic==2.5.0"  # Make sure pydantic is also up to date
    ]
    
    success = True
    for package in missing_packages:
        if not install_package(package):
            success = False
    
    if success:
        print("\n🎉 All missing dependencies installed!")
        print("\n📋 Now try running the backend again:")
        print("python start_backend_debug.py")
    else:
        print("\n❌ Some dependencies failed to install")
        print("Try running: python fix_python312.py")

if __name__ == "__main__":
    main() 