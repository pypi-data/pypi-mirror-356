"""
Test package initialization.
"""
import os
import sys

# Add the parent directory to sys.path to ensure we can import from core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))