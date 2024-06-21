.. servicepytan documentation master file, created by
   sphinx-quickstart on Sun Apr 10 17:50:18 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

servicepytan
========================================
A Python library for interacting with the ServiceTitan API v2
https://developer.servicetitan.io/

Pre-Requisites
--------------

Before you can use :code:`servicepytan`, you need to create and authorize your API application. The following link will walk you through the setup process.

* :doc:`ServicePytan Pre-Requisites <./prerequisites>`  

Installing ServicePytan
-----------------------

Recommended, create a virtual environment::

   # MacOS / Linux
   python -m venv .venv
   source ./.venv/bin/activate

   # Windows
   python -m venv .venv
   ./.venv/Scripts/activate

Install ServicePython from Github::

   pip install servicepytan

   # For the most up to date version
   pip install git+https://github.com/elliotpalmer/servicepytan
   
Create Configuration File
-------------------------

Create your :code:`servicepytan_config.json` file in the root directory::
   
   {
      "SERVICETITAN_CLIENT_ID": "cid.hhmdjd1jk9nqwertyr5cl6t5u5r5",
      "SERVICETITAN_CLIENT_SECRET": "cs2.yjnblmqpfiuzjyqwerty5gc28a35qabzo1qsss2l3fll5st64tgrxjxz",
      "SERVICETITAN_APP_ID": "12abc346skeg",
      "SERVICETITAN_APP_KEY": "ak1.qey12fgjhnch03lsm",
      "SERVICETITAN_TENANT_ID": "1234567890",
      "SERVICETITAN_TIMEZONE": ""
   }

Starting with >=0.3.0 there are addtioanl configuration options available. See :doc:`ServicePytan Configuration <./configuration>` for more information.
1. Create a .env file in the root directory of your project. This file will be used to store your environment variables.
2. By directly inputing the credentials into the :code:`servicepytan.auth.servicepytan_connect()` file, you are storing your credentials in plain text. This is not recommended.
> :code:`servicepytan.auth.servicepytan_connect(app_id="", app_key="", client_id="", client_secret="", tenant_id="", timezone="")`

> NOTE: Remember to exclude this file from version control. (e.g. add to your :code:`.gitignore` file)

* :code:`SERVICETITAN_CLIENT_ID` - Find in :code:`Settings > Integrations > API Application Access > [App Name] > Edit`
* :code:`SERVICETITAN_CLIENT_SECRET` - Generated one time with :code:`CLIENT ID`
* :code:`SERVICETITAN_APP_ID` - Found in developers portal app definition
* :code:`SERVICETITAN_APP_KEY` - Found in developers portal app definition
* :code:`SERVICETITAN_TENANT_ID` - Found in developers portal app definition and integration settings
* :code:`SERVICETITAN_TIMEZONE` - (Optional) - Timezone Abbreviation like :code:`America/New_York` as listed at https://timezonedb.com/time-zones

Making Your First Request
-------------------------

   Return the Job object by Job ID::

      import servicepytan

      # API Endpoint: https://api.servicetitan.io/jpm/v2/tenant/{tenant}/jobs
      # Folder: jpm, Endpoint: jobs

      # Create Connection Object. Note: This is a change from previous versions.
      st_conn = servicepytan.auth.servicepytan_connect(config_file="./servicepytan_config.json")
      
      # Create API Object
      st_jobs_endpoint = servicepytan.Endpoint("jpm", "jobs", conn=st_conn)

      # Return the data for a specific job in ServiceTitan
      # https://go.servicetitan.com/#/Job/Index/138517400
      job_json = st_jobs_endpoint.get_one(138517400)

      # Print the data to the console
      print(job_json)

   Data will return something like::
         
      {
         "id": 0,
         "jobNumber": "string",
         "customerId": 0,
         "locationId": 0,
         "jobStatus": "string",
         "completedOn": "string",
         ...
         "soldById": 0,
         "externalData": [{
            "key": "string",
            "value": "string"
         }]
      }

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents:

   prerequisites
   configuration
   examples
   servicepytan
   reference
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`