#!/usr/bin/env python

"""Tests for pandas integration in servicepytan."""

import unittest
import sys

# Skip tests if pandas is not available
try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class TestPandasIntegration(unittest.TestCase):
    """Tests for pandas integration."""

    def setUp(self):
        """Set up test fixtures, if any."""
        if not PANDAS_AVAILABLE:
            self.skipTest("pandas not available")

    def test_pandas_version(self):
        """Test that pandas version is 2.3.1 or higher."""
        self.assertGreaterEqual(pd.__version__, "2.3.1")
        print(f"Pandas version: {pd.__version__}")

    def test_numpy_version(self):
        """Test that numpy version is 1.24.0 or higher."""
        self.assertGreaterEqual(np.__version__, "1.24.0")
        print(f"NumPy version: {np.__version__}")

    def test_pandas_functionality(self):
        """Test basic pandas functionality."""
        # Create a simple DataFrame
        data = {
            'id': [1, 2, 3, 4, 5],
            'name': ['Job 1', 'Job 2', 'Job 3', 'Job 4', 'Job 5'],
            'status': ['Completed', 'In Progress', 'Completed', 'Scheduled', 'Completed']
        }
        df = pd.DataFrame(data)
        
        # Test basic operations
        self.assertEqual(len(df), 5)
        self.assertEqual(len(df.columns), 3)
        
        # Test filtering
        completed_jobs = df[df['status'] == 'Completed']
        self.assertEqual(len(completed_jobs), 3)
        
        # Test grouping
        status_counts = df['status'].value_counts()
        self.assertEqual(status_counts['Completed'], 3)
        self.assertEqual(status_counts['In Progress'], 1)
        self.assertEqual(status_counts['Scheduled'], 1)

    def test_python_version(self):
        """Test that Python version is 3.9 or higher."""
        version = sys.version_info
        self.assertGreaterEqual(version.major, 3)
        self.assertGreaterEqual(version.minor, 9)
        print(f"Python version: {version.major}.{version.minor}.{version.micro}")


if __name__ == '__main__':
    unittest.main()