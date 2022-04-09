"""Top-level package for servicepytan."""

__author__ = """Elliot Palmer"""
__email__ = 'elliot@ecoplumbers.com'
__version__ = '0.1.0'

# MODULES
import requests
import json

# GLOBALS
AUTH_ROOT = "https://auth.servicetitan.io"
URL_ROOT = "https://api.servicetitan.io"

from servicepytan.requests import Endpoint
from servicepytan.data import DataService
from servicepytan.dates import convert_date_to_api_format
