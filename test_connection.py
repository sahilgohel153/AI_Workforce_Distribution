#!/usr/bin/env python3
"""
Test script to check if backend is running
"""

import requests
import time
import sys

def test_backend():
    """Test if backend is accessible"""
    print("🔍 Testing backend connection...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and accessible!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend responded with status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running!")
        print("   Error: Connection refused")
        return False
    except requests.exceptions.Timeout:
        print("❌ Backend connection timed out!")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    print("🚀 Backend Connection Test")
    print("=" * 30)
    
    # Test multiple times
    for attempt in range(3):
        print(f"\n🔄 Attempt {attempt + 1}/3...")
        if test_backend():
            print("\n🎉 Backend is working correctly!")
            print("\n📋 Next steps:")
            print("1. Keep the backend running (don't close that window)")
            print("2. Open another terminal and run: python start_frontend.py")
            print("3. Open your browser and go to: http://localhost:8501")
            return True
        else:
            if attempt < 2:
                print("⏳ Waiting 2 seconds before retry...")
                time.sleep(2)
    
    print("\n❌ Backend is not accessible after 3 attempts")
    print("\n🔧 Troubleshooting steps:")
    print("1. Make sure you ran: python start_backend.py")
    print("2. Check if you see 'Uvicorn running on http://0.0.0.0:8000'")
    print("3. Make sure no other application is using port 8000")
    print("4. Try restarting your computer if the issue persists")
    return False

if __name__ == "__main__":
    main() 