#!/usr/bin/env python3
"""
Quick Start Script for TalentForge Pro
This script will help you get the project running quickly with sample data.
"""

import subprocess
import sys
import os
import time
import requests

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Start the backend server"""
    print("🚀 Starting TalentForge Pro Backend...")
    subprocess.Popen([sys.executable, "start_backend.py"])
    time.sleep(5)  # Wait for backend to start

def populate_sample_data():
    """Populate the database with sample data"""
    print("📊 Adding sample data to the database...")
    subprocess.run([sys.executable, "sample_data.py"])

def start_frontend():
    """Start the frontend"""
    print("🎨 Starting TalentForge Pro Frontend...")
    subprocess.run([sys.executable, "start_frontend.py"])

def main():
    print("""
    ⚡ TalentForge Pro - Quick Start
    ================================
    
    This script will:
    1. Start the backend server
    2. Add sample data
    3. Start the frontend
    4. Open your browser
    
    """)
    
    # Check if backend is already running
    if check_backend():
        print("✅ Backend is already running!")
    else:
        print("🔄 Starting backend server...")
        start_backend()
        
        # Wait for backend to be ready
        print("⏳ Waiting for backend to be ready...")
        for i in range(30):  # Wait up to 30 seconds
            if check_backend():
                print("✅ Backend is ready!")
                break
            time.sleep(1)
        else:
            print("❌ Backend failed to start. Please check the logs.")
            return
    
    # Add sample data
    populate_sample_data()
    
    print("""
    🎉 Setup Complete!
    =================
    
    Your TalentForge Pro application is now ready!
    
    🌐 Frontend: http://localhost:8501
    🔌 Backend: http://localhost:8000
    📚 API Docs: http://localhost:8000/docs
    
    The application will open in your browser automatically.
    """)
    
    # Start frontend
    start_frontend()

if __name__ == "__main__":
    main() 