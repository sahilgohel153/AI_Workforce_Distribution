#!/usr/bin/env python3
"""
Startup script for Workforce Distribution.ai Backend
"""

import uvicorn
import os
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == "__main__":
    print("🚀 Starting Workforce Distribution.ai Backend...")
    print("📊 API will be available at: http://localhost:8000")
    print("📚 Documentation will be available at: http://localhost:8000/docs")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 