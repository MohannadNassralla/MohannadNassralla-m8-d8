"""Pytest config — adds the repo root to sys.path so tests/ can import lab."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
