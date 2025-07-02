#!/usr/bin/env python

"""Tests for `servicepytan` package."""

import unittest
from click.testing import CliRunner

import servicepytan
from servicepytan import cli


class TestServicepytan(unittest.TestCase):
    """Tests for `servicepytan` package."""

    def test_package_imports(self):
        """Test that package imports work correctly."""
        # Test main imports
        self.assertTrue(hasattr(servicepytan, 'Endpoint'))
        self.assertTrue(hasattr(servicepytan, 'Report'))
        self.assertTrue(hasattr(servicepytan, 'DataService'))
        
        # Test version
        self.assertTrue(hasattr(servicepytan, '__version__'))
        self.assertEqual(servicepytan.__version__, '0.3.2')

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('ServicePytan CLI', result.output)
        self.assertIn('--help', result.output)

    def test_cli_init_command(self):
        """Test CLI init command."""
        runner = CliRunner()
        result = runner.invoke(cli.main, ['init', '--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Initialize ServicePytan configuration', result.output)

    def test_cli_list_endpoints_command(self):
        """Test CLI list-endpoints command."""
        runner = CliRunner()
        result = runner.invoke(cli.main, ['list-endpoints'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Job Planning & Management', result.output)
        self.assertIn('jobs', result.output)
