"""
Quick Start Script for Smart Panchayat AI System
Automated setup and launch
"""
import subprocess
import sys
import os
import time

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(cmd, description):
    print(f"➤ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"  ✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error: {e}")
        print(f"  Output: {e.output}")
        return False

def check_python():
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ required")
        return False
    print("✓ Python version is compatible")
    return True

def main():
    print_header("Smart Panchayat AI - Quick Start")

    # Check Python version
    if not check_python():
        return

    # Check if we're in the right directory
    if not os.path.exists("backend"):
        print("❌ Error: Please run this script from the smart-panchayat-ai directory")
        return

    # Step 1: Install dependencies
    print_header("Step 1: Installing Dependencies")
    if run_command("pip install -r requirements.txt", "Installing Python packages"):
        print("✓ All dependencies installed")
    else:
        print("❌ Failed to install dependencies. Please run manually: pip install -r requirements.txt")
        return

    # Step 2: Initialize database
    print_header("Step 2: Initializing Database")
    if run_command("python backend/init_db.py", "Creating database and seeding wards/schemes"):
        print("✓ Database initialized")
    else:
        print("⚠ Database initialization had issues. Continuing...")

    # Step 3: Seed demo data
    print_header("Step 3: Generating Demo Data")
    response = input("Generate synthetic demo data? (recommended) [Y/n]: ").strip().lower()
    if response != 'n':
        if run_command("python backend/seed_demo_data.py", "Generating households, members, and issues"):
            print("✓ Demo data created successfully")
        else:
            print("⚠ Demo data generation had issues. You can add data manually via the portal.")

    # Step 4: Instructions to start servers
    print_header("Setup Complete! 🎉")
    print("""
Next Steps - Start the servers in separate terminals:

Terminal 1 - Backend API:
  cd backend
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Terminal 2 - Family Head Portal:
  cd frontend
  streamlit run family_portal.py --server.port 8501

Terminal 3 - Sarpanch Dashboard:
  cd frontend
  streamlit run sarpanch_dashboard.py --server.port 8502

Then access:
  - API Docs: http://localhost:8000/docs
  - Family Portal: http://localhost:8501
  - Sarpanch Dashboard: http://localhost:8502

For detailed instructions, see README.md
    """)

    start_servers = input("\nDo you want to start all servers now? [y/N]: ").strip().lower()
    if start_servers == 'y':
        print("\n⚠ Note: This will open 3 terminal windows. Close them when done.")
        time.sleep(2)

        # Start backend
        if sys.platform == "win32":
            subprocess.Popen("start cmd /k cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000", shell=True)
            time.sleep(3)
            subprocess.Popen("start cmd /k cd frontend && streamlit run family_portal.py --server.port 8501", shell=True)
            time.sleep(2)
            subprocess.Popen("start cmd /k cd frontend && streamlit run sarpanch_dashboard.py --server.port 8502", shell=True)
        else:
            print("Auto-start only supported on Windows. Please start servers manually.")

    print("\n✨ Smart Panchayat AI is ready!")

if __name__ == "__main__":
    main()
