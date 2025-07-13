#!/usr/bin/env python3
"""
Debug startup script for Workforce Distribution.ai Backend
"""

import uvicorn
import os
import sys
import subprocess
import socket

def check_port_available(port):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def kill_process_on_port(port):
    """Kill process using the specified port"""
    try:
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True, capture_output=True, text=True
        )
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if f':{port}' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        print(f"🔄 Killing process {pid} on port {port}")
                        subprocess.run(f'taskkill /PID {pid} /F', shell=True)
                        return True
    except Exception as e:
        print(f"⚠️  Could not kill process on port {port}: {e}")
    return False

def main():
    print("🚀 Starting Workforce Distribution.ai Backend (Debug Mode)...")
    print("=" * 60)
    
    # Check Python path
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"🐍 Python path: {sys.path[:3]}...")
    
    # Add backend to path
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    sys.path.append(backend_path)
    print(f"📂 Added backend path: {backend_path}")
    
    # Check if backend directory exists
    if not os.path.exists(backend_path):
        print(f"❌ Backend directory not found: {backend_path}")
        return False
    
    # Check if main.py exists
    main_file = os.path.join(backend_path, 'app', 'main.py')
    if not os.path.exists(main_file):
        print(f"❌ Main file not found: {main_file}")
        return False
    
    print(f"✅ Main file found: {main_file}")
    
    # Check port availability
    port = 8000
    if not check_port_available(port):
        print(f"⚠️  Port {port} is already in use")
        if kill_process_on_port(port):
            print(f"✅ Killed process on port {port}")
        else:
            print(f"❌ Could not free port {port}")
            return False
    else:
        print(f"✅ Port {port} is available")
    
    # Test imports
    print("\n🔍 Testing imports...")
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        print("💡 Run: python fix_python312.py")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        print("💡 Run: python fix_python312.py")
        return False
    
    # Try to import the app
    try:
        sys.path.insert(0, backend_path)
        from app.main import app
        print("✅ App imported successfully")
    except ImportError as e:
        print(f"❌ App import failed: {e}")
        print("💡 Check if all dependencies are installed")
        return False
    
    print("\n🎯 Starting server...")
    print("📊 API will be available at: http://localhost:8000")
    print("📚 Documentation will be available at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server failed to start: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 