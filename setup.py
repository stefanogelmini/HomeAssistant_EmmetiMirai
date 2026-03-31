"""Setup for Emmeti Mirai Home Assistant integration."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="emmeti-mirai-ha",
    version="1.0.0",
    author="Stefano Gelmini",
    author_email="stefanogelmini@gmail.com",
    description="Emmeti Mirai Home Assistant Integration - Modbus TCP support",
    long_description="Custom integration per interfacciare la pompa di calore Emmeti Mirai tramite Modbus TCP con Home Assistant.",
    long_description_content_type="text/markdown",
    url="https://github.com/stefanogelmini/Emmeti_Mirai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Home Automation",
    ],
    python_requires=">=3.11",
    install_requires=[
        "pymodbus>=3.0.0",
    ],
)
