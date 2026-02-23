"""Shared base test utilities for hotel reservation test suite."""

import os
import unittest
from unittest.mock import patch


class BaseTempFileTest(unittest.TestCase):
    """Base class that patches a DATA_FILE to a temp path for each test."""

    module = None
    temp_file = None

    def setUp(self):
        """Patch DATA_FILE to a temp file and print test description."""
        print(f"\n▶  {self._testMethodName}: {self._testMethodDoc}")
        self.patcher = patch.object(self.module, 'DATA_FILE', self.temp_file)
        self.patcher.start()
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def tearDown(self):
        """Stop patcher and remove temp file after each test."""
        self.patcher.stop()
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
