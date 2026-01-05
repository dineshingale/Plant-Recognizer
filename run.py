#!/usr/bin/env python3
"""
Plant Recognizer - Automatic Setup and Server Launcher
This script installs requirements and starts the FastAPI Backend.
"""

import subprocess
import sys
import os
import time

def install_requirements():
    """Install all required packages from requirements.txt"""
    print("\n" + "="*60)
    print("🌿 Plant Recognizer - Dependency Installation")
    print("="*60 + "\n")
    
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    if not os.path.exists(requirements_path):
        print("❌ Error: requirements.txt not found!")
        sys.exit(1)
    
    print("📦 Installing/Verifying required packages...")
    print("-" * 60)
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        print("\n✅ Dependencies ready!\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error installing packages: {e}")
        sys.exit(1)

def run_server():
    """Run the FastAPI Server"""
    server_path = os.path.join(os.path.dirname(__file__), 'server.py')
    
    if not os.path.exists(server_path):
        print(f"❌ Error: server.py not found at {server_path}")
        sys.exit(1)
    
    print("🚀 Starting Backend Server...")
    print(f"📡 API will be available at: http://localhost:8000")
    print("="*60 + "\n")
    
    try:
        # Run server.py using the current python executable
        subprocess.run([sys.executable, server_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Server stopped by user")
        sys.exit(0)

def main():
    try:
        install_requirements()
        
        print("ℹ️  Note: Please ensure the React Client is running in a separate terminal:")
        print("   cd Client && npm run dev\n")
        time.sleep(2)
        
        run_server()
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
