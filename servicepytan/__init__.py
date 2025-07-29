"""A high-level package for ineracting with the ServiceTitan API v2.

ServicePytan provides an API for easily constructing requests to the ServiceTitan API v2.
The `Endpoint` class is the primary means to constructing requests based on the organization detailed
on developer site.

  Resources:
    - https://developer.servicetitan.io

  Examples:
    >>> import servicepytan
    >>> servicetitan_endpoint = servicepytan.Endpoint("jpm","jobs")
    >>> data = servicetitan_endpoint.get_one(id=12345678)
"""

__author__ = """Elliot Palmer"""
__email__ = "elliot@ecoplumbers.com"
__version__ = "0.3.2"

# MODULES
from servicepytan.requests import Endpoint
from servicepytan.reports import Report
from servicepytan.data import DataService
from servicepytan.auth import servicepytan_connect

__all__ = [
    "Endpoint",
    "Report",
    "DataService",
    "servicepytan_connect",
]
