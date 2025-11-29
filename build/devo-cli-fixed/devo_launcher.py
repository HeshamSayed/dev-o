#!/usr/bin/env python3
"""
Simple launcher for Devo CLI
"""
import sys
import os

# Add CLI directory to Python path
cli_dir = os.path.dirname(os.path.abspath(__file__))
if cli_dir not in sys.path:
    sys.path.insert(0, cli_dir)

# Change to CLI directory
os.chdir(cli_dir)

# Now execute the main module
if __name__ == "__main__":
    from main import app
    app()
