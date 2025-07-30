from setuptools import setup, find_packages

setup(
    name="darktrace",
    version="1.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "cryptography",
        "requests",
        "Pillow",
        "pyttsx3",
        "openai",
        "keyboard",
        "beautifulsoup4",
        "simpleaudio",
        "pyaudio",
        "getpass4",
        "langdetect",
        "googletrans==4.0.0rc1",
        "lxml"
    ],
    entry_points={
        "console_scripts": [
            "darktrace = darktrace_locks.__init__:run",
        ],
    },
    author="CURE",
    description="DARKTRACE: Advanced Secure Lock & Reverse Search System with AI Assistant",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/CURE0FFICIAL/darktrace-locks",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
