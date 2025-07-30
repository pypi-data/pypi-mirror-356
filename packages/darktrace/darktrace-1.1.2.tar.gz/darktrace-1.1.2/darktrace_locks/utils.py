# darktrace_locks/utils.py

import os
import json
import base64
import getpass
from tkinter import Tk, filedialog
from cryptography.fernet import Fernet
from PIL import Image

# === Credential Handling ===
CREDENTIALS_FILE = "credentials.dat"

def save_credentials(data: dict):
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(data, f)

def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            return json.load(f)
    return {}

def mask_input(prompt=""):
    return getpass.getpass(prompt)

# === Encryption Utilities ===
def load_key():
    return open("secret.key", "rb").read()

def encrypt_file(file_path, key=None):
    if not key:
        key = load_key()
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        data = file.read()
    encrypted = fernet.encrypt(data)
    with open(file_path + ".enc", "wb") as file:
        file.write(encrypted)

def decrypt_file(file_path, key=None):
    if not key:
        key = load_key()
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        data = file.read()
    decrypted = fernet.decrypt(data)
    with open(file_path.replace(".enc", ""), "wb") as file:
        file.write(decrypted)

# === Image Helpers ===
def select_image_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    return file_path

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def resize_image(image_path, size=(128, 128)):
    with Image.open(image_path) as img:
        img = img.resize(size)
        resized_path = os.path.splitext(image_path)[0] + "_resized.png"
        img.save(resized_path)
        return resized_path
