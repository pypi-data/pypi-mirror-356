#!/usr/bin/env python3
"""
Setup script for AirTag Detector package
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="airtag-detector",
    version="1.0.0",
    author="DogPi Project",
    author_email="contras-kite9t@icloud.com",
    description="Apple AirTag detector for Raspberry Pi with HomeKit integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nranderson/dogpi",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Home Automation",
        "Topic :: Security",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Environment :: No Input/Output (Daemon)",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "homekit": ["aiohomekit>=3.1.0"],
        "dev": ["pytest>=7.0", "black", "flake8", "mypy"],
    },
    entry_points={
        "console_scripts": [
            "airtag-detector=airtag_detector.detector:main",
            "airtag-setup=airtag_detector.setup:main",
            "airtag-homekit-setup=airtag_detector.homekit_setup:main",
            "airtag-test=airtag_detector.test_bluetooth:main",
        ],
    },
    include_package_data=True,
    package_data={
        "airtag_detector": [
            "templates/*.service",
            "configs/*.py.template",
        ],
    },
    data_files=[
        ("share/airtag-detector/systemd", ["airtag_detector/templates/airtag-detector.service"]),
        ("share/airtag-detector/configs", ["airtag_detector/configs/config.py.template"]),
    ],
    zip_safe=False,
    keywords="airtag bluetooth raspberry-pi homekit home-automation security tracking-detection",
    project_urls={
        "Bug Reports": "https://github.com/nranderson/dogpi/issues",
        "Source": "https://github.com/nranderson/dogpi",
        "Documentation": "https://github.com/nranderson/dogpi/blob/main/README.md",
    },
)
