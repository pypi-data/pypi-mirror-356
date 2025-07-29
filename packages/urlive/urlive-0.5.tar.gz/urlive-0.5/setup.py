from setuptools import setup, find_packages
import sys
import platform

def check_tkinter():
    if platform.system() == "Linux":
        try:
            import tkinter
        except ImportError:
            print("\n[!] Missing required system package: tkinter")
            print("👉 Try installing it using:")
            print("   sudo apt install python3-tk\n")
            sys.exit(1)

# Run tkinter check before setup
check_tkinter()

setup(
    name="urlive",
    version="0.5",
    description="A URL status checker by GTSivam",
    author="Thirumurugan (GTSivam)",
    author_email="gtsivam6@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.3.0",
    ],
    python_requires=">=3.8, <4.0",
    entry_points={
        'console_scripts': [
            'urlive=urlive.main:run_app',
        ],
    },
)

