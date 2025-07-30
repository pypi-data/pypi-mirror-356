# darktrace_locks/setup_mode.py

import os
import json
import getpass
from cryptography.fernet import Fernet
from .utils import save_credentials, load_key, select_image_file

CREDENTIALS_FILE = "credentials.dat"
ENCRYPTED_FILE = "data.enc"

def setup_encryption():
    print("🔧 DARKTRACE Setup Mode")
    
    # Pattern setup
    pattern = input("🔢 Set your pattern (numbers only): ").strip()
    
    # Password setup
    password = getpass.getpass("🔐 Set your password (hidden): ").strip()
    
    # Security Q&A
    q1 = input("❓ Question 1 (e.g. 'Is Elon Musk a thief?') → ").strip()
    a1 = input("🔑 Answer → ").strip()
    
    q2 = input("❓ Question 2 (e.g. 'Egg or Omelet?') → ").strip()
    a2 = input("🔑 Answer → ").strip()

    # App password input (optional)
    app_password = getpass.getpass("📧 Enter your Gmail App Password (used for OTP): ").strip()
    
    # Name or Photo upload
    choice = input("👤 Do you want to (1) Enter Name or (2) Upload Image? [1/2]: ").strip()
    user_name = ""
    image_path = ""

    if choice == "1":
        user_name = input("👥 Enter your name: ").strip()
    elif choice == "2":
        print("🖼️ Select an image for reverse image search...")
        image_path = select_image_file()
    else:
        print("⚠️ Invalid choice, skipping.")

    # Encrypt a sample file to simulate protection
    key = load_key()
    fernet = Fernet(key)
    sample_data = "This is protected info.".encode()
    encrypted = fernet.encrypt(sample_data)
    with open(ENCRYPTED_FILE, "wb") as f:
        f.write(encrypted)

    # Save everything securely
    save_credentials({
        "pattern": pattern,
        "password": password,
        "security_questions": {
            q1: a1,
            q2: a2
        },
        "app_password": app_password,
        "name": user_name,
        "image": image_path
    })

    print("✅ Setup complete. You can now run DARKTRACE normally.")
