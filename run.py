#!/usr/bin/env python3
"""
Flower Recognizer - Automatic Setup and Run Script
This script installs all required packages and runs the main application
"""

import subprocess
import sys
import os

def install_requirements():
    """Install all required packages from requirements.txt"""
    print("\n" + "="*60)
    print("🌼 Flower Recognizer - Dependency Installation")
    print("="*60 + "\n")
    
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    if not os.path.exists(requirements_path):
        print("❌ Error: requirements.txt not found!")
        print(f"Expected location: {requirements_path}")
        sys.exit(1)
    
    print("📦 Installing required packages...")
    print("-" * 60)
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        print("\n" + "-" * 60)
        print("✅ All packages installed successfully!\n")
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "-" * 60)
        print(f"❌ Error installing packages: {e}")
        print("Please try installing manually with:")
        print(f"   pip install -r {requirements_path}")
        sys.exit(1)

def run_main():
    """Run the main.py script"""
    main_path = os.path.join(os.path.dirname(__file__), 'src', 'main.py')
    
    if not os.path.exists(main_path):
        print(f"❌ Error: main.py not found at {main_path}")
        sys.exit(1)
    
    print("🚀 Starting Flower Recognition System...\n")
    print("="*60 + "\n")
    
    try:
        subprocess.run([sys.executable, main_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running main.py: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrupted by user")
        sys.exit(0)

def main():
    """Main execution flow"""
    try:
        # Install dependencies
        install_requirements()
        
        # Run the main application
        run_main()
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
