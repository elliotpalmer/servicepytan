============
servicepytan
============


.. image:: https://img.shields.io/pypi/v/servicepytan.svg
        :target: https://pypi.python.org/pypi/servicepytan

.. image:: https://github.com/elliotpalmer/servicepytan/workflows/Test/badge.svg
        :target: https://github.com/elliotpalmer/servicepytan/actions

.. image:: https://readthedocs.org/projects/servicepytan/badge/?version=latest
        :target: https://servicepytan.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/servicepytan.svg
        :target: https://pypi.python.org/pypi/servicepytan

.. image:: https://codecov.io/gh/elliotpalmer/servicepytan/branch/main/graph/badge.svg
        :target: https://codecov.io/gh/elliotpalmer/servicepytan


Python Library to make it easier to interact with the ServiceTitan API v2

A modern, robust Python library for ServiceTitan API v2 with intelligent caching, comprehensive error handling, and a powerful CLI interface.

* Free software: MIT license
* Documentation: https://servicepytan.readthedocs.io.
* Python 3.8+ support


Features
--------

**Core Functionality**
* Simple syntax for getting data from standard RESTful endpoints from ServiceTitan
* Ability to extract custom report data and automatically make calls for additional data
* Intelligent authentication token caching with automatic expiration handling
* Comprehensive retry logic with exponential backoff for transient errors
* Support for all major ServiceTitan API endpoints (Jobs, Sales, Inventory, Settings, etc.)

**Command Line Interface**
* Full-featured CLI for testing and data extraction
* Easy configuration management
* Built-in endpoint discovery and documentation
* Multiple output formats (JSON, CSV, table)

**Developer Experience**
* Comprehensive test suite with high coverage
* Type hints and modern Python practices
* Detailed error messages and debugging support
* Pre-commit hooks and code quality tools

**Security & Reliability**
* Secure credential management
* No credentials exposed in logs
* Automatic rate limiting compliance
* Connection pooling and retry mechanisms

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
