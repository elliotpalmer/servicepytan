.. servicepytan documentation master file, created by
   sphinx-quickstart on Sun Apr 10 17:50:18 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ServicePytan
============================================

**A comprehensive Python library for interacting with the ServiceTitan API v2**

ServicePytan provides a simple, Pythonic interface to the ServiceTitan API, making it easy to retrieve data, 
manage reports, and integrate ServiceTitan with your applications. Built with developers in mind, it handles 
authentication, pagination, rate limiting, and provides both low-level endpoint access and high-level 
convenience methods.

.. note::
   **Current Version: 0.3.2** - This documentation covers all features available in the latest release.

Key Features
------------

✅ **Simple Authentication** - Multiple configuration options including JSON files, environment variables, and direct parameters

✅ **Environment Support** - Switch between production and integration environments seamlessly  

✅ **Comprehensive API Coverage** - Access any ServiceTitan API endpoint with the flexible Endpoint class

✅ **High-Level Data Services** - Simplified methods for common data operations like retrieving jobs, customers, and invoices

✅ **Advanced Reporting** - Full support for ServiceTitan's custom reports with automatic pagination

✅ **Automatic Pagination** - Built-in handling of paginated responses with `get_all()` methods

✅ **Error Handling** - Robust error handling with detailed logging and retry mechanisms

✅ **Date/Time Management** - Intelligent timezone handling and date formatting

Quick Start
-----------

Install ServicePytan::

   pip install servicepytan

   # For the latest development version
   pip install git+https://github.com/elliotpalmer/servicepytan

Create a connection and make your first request::

   import servicepytan

   # Create connection (multiple options available - see Configuration section)
   conn = servicepytan.auth.servicepytan_connect(config_file="config.json")
   
   # Get a specific job
   jobs_endpoint = servicepytan.Endpoint("jpm", "jobs", conn=conn)
   job = jobs_endpoint.get_one(138517400)
   
   # Or use the simplified DataService
   data_service = servicepytan.DataService(conn=conn)
   recent_jobs = data_service.get_jobs_completed_between("2024-01-01", "2024-01-31")

Prerequisites
-------------

Before using ServicePytan, you need:

1. **ServiceTitan API Application** - Set up through the ServiceTitan Developer Portal
2. **API Credentials** - Client ID, Client Secret, App ID, App Key, and Tenant ID
3. **Python 3.6+** - ServicePytan supports Python 3.6 and higher

For detailed setup instructions, see:

* :doc:`ServicePytan Prerequisites <./prerequisites>`  

Installation & Configuration
----------------------------

ServicePytan offers flexible configuration options to suit different deployment scenarios:

**JSON Configuration File** (Recommended for development)::

   {
      "SERVICETITAN_CLIENT_ID": "cid.example123",
      "SERVICETITAN_CLIENT_SECRET": "cs2.example456", 
      "SERVICETITAN_APP_ID": "12345",
      "SERVICETITAN_APP_KEY": "ak1.example789",
      "SERVICETITAN_TENANT_ID": "1234567890",
      "SERVICETITAN_TIMEZONE": "America/New_York",
      "SERVICETITAN_API_ENVIRONMENT": "production"
   }

**Environment Variables** (Recommended for production)::

   # Set in your .env file or environment
   export SERVICETITAN_CLIENT_ID="your_client_id"
   export SERVICETITAN_CLIENT_SECRET="your_client_secret"
   export SERVICETITAN_APP_KEY="your_app_key"
   export SERVICETITAN_TENANT_ID="your_tenant_id"
   export SERVICETITAN_API_ENVIRONMENT="production"

**Direct Parameters** (For dynamic configurations)::

   conn = servicepytan.auth.servicepytan_connect(
       client_id="your_client_id",
       client_secret="your_client_secret",
       app_key="your_app_key", 
       tenant_id="your_tenant_id",
       api_environment="production"
   )

For complete configuration details, see:

* :doc:`Configuration Guide <./configuration>`

API Access Patterns
-------------------

ServicePytan provides three main patterns for accessing ServiceTitan data:

**1. Endpoint Class** - Direct API access with full control::

   # Access any ServiceTitan endpoint
   endpoint = servicepytan.Endpoint("folder", "endpoint_name", conn=conn)
   
   # Get single record
   record = endpoint.get_one(record_id)
   
   # Get all records with automatic pagination
   all_records = endpoint.get_all(query_parameters)
   
   # Create, update, delete operations
   new_record = endpoint.post(data)
   updated_record = endpoint.patch(record_id, data)

**2. DataService Class** - Simplified high-level operations::

   data_service = servicepytan.DataService(conn=conn)
   
   # Common data operations with intelligent defaults
   jobs = data_service.get_jobs_completed_between("2024-01-01", "2024-01-31")
   customers = data_service.get_customers_created_between("2024-01-01", "2024-01-31")
   invoices = data_service.get_invoices_completed_between("2024-01-01", "2024-01-31")

**3. Report Class** - Advanced custom reporting::

   # Access ServiceTitan's custom reports
   report = servicepytan.Report("operations", "report_id", conn=conn)
   report.add_params("From", "2024-01-01")
   report.add_params("To", "2024-01-31")
   
   # Get all report data with automatic pagination
   report_data = report.get_all_data()

Environment Support
------------------

ServicePytan supports both ServiceTitan environments:

* **Production** - Live data environment (default)
* **Integration** - Testing environment for development

Switch environments easily::

   # Production (default)
   conn = servicepytan.auth.servicepytan_connect(api_environment="production")
   
   # Integration/Testing
   conn = servicepytan.auth.servicepytan_connect(api_environment="integration")

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   prerequisites
   configuration

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   examples
   troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   servicepytan
   reference

.. toctree::
   :maxdepth: 2
   :caption: Deployment:

   deployment

Community & Support
------------------

* **GitHub Repository**: https://github.com/elliotpalmer/servicepytan
* **Issue Tracker**: https://github.com/elliotpalmer/servicepytan/issues
* **PyPI Package**: https://pypi.org/project/servicepytan/
* **ServiceTitan Developer Docs**: https://developer.servicetitan.io/

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`