"""Pytest/unittest configuration: adds project root to sys.path."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
