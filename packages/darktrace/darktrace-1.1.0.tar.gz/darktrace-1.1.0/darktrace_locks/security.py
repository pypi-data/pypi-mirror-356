# darktrace_locks/security.py

import getpass
import os
from cryptography.fernet import Fernet
from .utils import load_key, decrypt_data
from .email_handler import send_otp_email
from .reverse_image import run_image_search

def run_security_check():
    print("🔐 Welcome to DARKTRACE Authentication")

    pattern = input("Enter pattern: ")
    password = getpass.getpass("Enter password: ")

    key = load_key()

    # Load credentials
    try:
        with open("credentials.dat", "r") as f:
            lines = f.readlines()
            enc_pattern = lines[0].strip().encode()
            enc_password = lines[1].strip().encode()
            enc_q1 = lines[2].strip().encode()
            enc_q2 = lines[3].strip().encode()
    except FileNotFoundError:
        print("❌ Encrypted credentials not found. Run setup first.")
        return

    real_pattern = decrypt_data(enc_pattern, key)
    real_password = decrypt_data(enc_password, key)
    q1 = decrypt_data(enc_q1, key)
    q2 = decrypt_data(enc_q2, key)

    if pattern == real_pattern and password == real_password:
        sec1 = input("Is elon musk a thief?: ")
        sec2 = input("Egg or omlet?: ")

        if sec1.lower() != q1.lower() or sec2.lower() != q2.lower():
            print("❌ Security questions failed.")
            return

        print("✅ Access granted. Welcome to DARKTRACE.")
        decrypted = decrypt_data(b'gAAAAABoUkNrEr8BHuaSnoaP-UVxldWESUr-TrJcNgziFL4cIUlDD2BmE2g_UHTZa50PywoAOHOjRWDqqjxe4YDgMKzHxI37L5Bp1-50apjQlX1km7wnawA=', key)
        print("🔓 Decrypted:", decrypted)

        # Reverse image search
        run_image_search()

    else:
        print("❌ Access denied.")

