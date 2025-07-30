
# darktrace_locks/core.py

import sys
from getpass import getpass
from .security import run_security_check

def main():
    if "--setup" in sys.argv:
        from . import setup_mode
        setup_mode.setup_encryption()
    else:
        print("🔐 Welcome to DARKTRACE Authentication")
        run_security_check()
