#!/usr/bin/env python3
"""
Fix script for Python 3.12 compatibility issues
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🔧 Python 3.12 Compatibility Fix")
    print("=" * 40)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major == 3 and python_version.minor == 12:
        print("✅ Detected Python 3.12 - applying compatibility fixes...")
    else:
        print("⚠️  Not Python 3.12, but continuing with fixes anyway...")
    
    # Step 1: Upgrade pip
    if not run_command("python -m pip install --upgrade pip", "Upgrading pip"):
        print("⚠️  Pip upgrade failed, but continuing...")
    
    # Step 2: Install setuptools and wheel first
    if not run_command("python -m pip install --upgrade setuptools wheel", "Installing setuptools and wheel"):
        print("❌ Failed to install setuptools and wheel. This is critical!")
        return False
    
    # Step 3: Install packages one by one to avoid conflicts
    packages = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0", 
        "sqlalchemy==2.0.23",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "pandas==2.1.4",
        "numpy==1.25.2",
        "streamlit==1.28.2",
        "plotly==5.17.0",
        "matplotlib==3.8.2",
        "seaborn==0.13.0",
        "requests==2.31.0",
        "httpx==0.25.2",
        "python-multipart==0.0.6",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-dotenv==1.0.0",
        "scikit-learn==1.3.2",
        "alembic==1.12.1",
        "psycopg2-binary==2.9.9",
        "pytest==7.4.3",
        "pytest-asyncio==0.21.1"
    ]
    
    print(f"\n📦 Installing {len(packages)} packages...")
    
    for i, package in enumerate(packages, 1):
        print(f"\n📦 [{i}/{len(packages)}] Installing {package}...")
        if not run_command(f"python -m pip install {package}", f"Installing {package}"):
            print(f"⚠️  Failed to install {package}, but continuing...")
    
    # Step 4: Verify key packages
    print("\n🔍 Verifying key packages...")
    key_packages = ["fastapi", "uvicorn", "streamlit", "pandas", "numpy"]
    
    for package in key_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - NOT FOUND")
    
    print("\n🎉 Installation completed!")
    print("\n📋 Next steps:")
    print("1. Run: python start_backend.py")
    print("2. Open another terminal and run: python start_frontend.py")
    print("3. Open your browser and go to: http://localhost:8501")

if __name__ == "__main__":
    main() 