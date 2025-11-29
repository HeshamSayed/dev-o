"""
Setup configuration for DEVO CLI.
"""
from setuptools import setup, find_packages
import os

# Read requirements.txt if it exists, otherwise use hardcoded list
requirements = [
    "typer>=0.9.0",
    "rich>=13.7.0",
    "httpx>=0.25.2",
    "websockets>=12.0",
    "pydantic>=2.5.3",
    "pydantic-settings>=2.1.0",
    "python-dotenv>=1.0.0",
]

if os.path.exists("requirements.txt"):
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()

setup(
    name="devo-cli",
    version="0.1.0",
    description="DEVO - Multi-Agent AI Development System CLI",
    author="DEVO Team",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "devo=devo.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
