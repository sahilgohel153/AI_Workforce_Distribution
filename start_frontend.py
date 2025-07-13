#!/usr/bin/env python3
"""
Startup script for Workforce Distribution.ai Frontend
"""

import subprocess
import sys
import os

if __name__ == "__main__":
    print("🎨 Starting Workforce Distribution.ai Frontend...")
    print("🌐 Streamlit will be available at: http://localhost:8501")
    
    # Change to the frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(frontend_dir)
    
    # Start Streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ]) 