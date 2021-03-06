"""Utility Functions for Supporting Other Modules"""
import requests
import json
import inspect
from servicepytan import URL_ROOT, AUTH_ROOT
from servicepytan.auth import get_auth_headers, get_tenant_id

def request_json(url, options={}, payload="", config_file='servicepytan_config.json', request_type="GET"):
  """Makes the request to the API and returns JSON

  Retrives JSON response from provided URL with a number of parameters to customize the request.

  Args:
      url: A string with the full URL request
      options: A dictionary defining the parameters to add to the url for filtering
      payload: A dictionary defining the data object to create or update
      config_file: A string for the file path to the configuration file.
      request_type: A string to define the REST endpoint type [GET, POST, PUT, PATCH, DEL].

  Returns:
      JSON Object

  Raises:
      TBD
  """
  headers = get_auth_headers(config_file)
  response = requests.request(request_type, url, data=payload, headers=headers, params=options)
  return json.loads(response.text)

def check_default_options(options):
  """Add sensible defaults to options when not defined"""
  # TODO: Add ability to read from a configuration file
  if "pageSize" not in options:
    options["pageSize"] = 100
  
  return options

def endpoint_url(folder, endpoint, id="", modifier="", config_file='servicepytan_config.json', tenant_id=""):
  """Constructs API request URL based on key parameters

  Retrives JSON response from provided URL with a number of parameters to customize the request.

  Args:
      folder: A string based on the endpoint groupings
      endpoint: A string indicating the endpoint you want to address.
      id: A string for the id of the endpoint object you're addressing.
      modifier: A string to modify the url to address the additional endpoint.
      config_file: A string for the file path to the configuration file.
      tenant_id: A string to manually adjust the tenant id.

  Returns:
      A URL String

  Raises:
      TBD
  """  
  # Adds ability to manually switch up the Tenant ID for apps that have multiples
  if tenant_id == "":
    tenant_id = get_tenant_id(config_file)

  url = f"{URL_ROOT}/{folder}/v2/tenant/{tenant_id}/{endpoint}"
  if id != "": url = f"{url}/{id}"
  if modifier != "": url = f"{url}/{modifier}"
  return url
    
def create_credential_file(name="servicepytan_config.json"):
  """Creates and saves an unfilled configuration file.

  Args:
      name: A string path to the credentials file

  Returns:
      A filepath string
  """  
  file = open(name, 'w')
  file.write(
    """{
    "CLIENT_ID": "",
    "CLIENT_SECRET": "",
    "APP_ID": "",
    "APP_KEY": "",
    "TENANT_ID": ""
    }"""
  )
  file.close()
  return name

def get_timezone_by_file(config_file='servicepytan_config.json'):
  """Retrieves timezone from the configuration file.

  Args:
      config_file: A string path to the credentials file

  Returns:
      Timezone string
  """    
  # Read File
  f = open(config_file)
  config = json.load(f)
  if "TIMEZONE" in config:
    timezone = config['TIMEZONE']
  else:
    timezone = ""
  f.close()
  return timezone