"""Utility Functions for Supporting Other Modules"""
import requests
import time
from servicepytan.auth import get_auth_headers, get_tenant_id

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

def request_json(url, options={}, payload={}, conn=None, request_type="GET", json_payload={}):
  """Makes the request to the API and returns JSON.

  Sends HTTP requests to the ServiceTitan API with proper authentication headers
  and handles various request types including GET, POST, PUT, PATCH, and DELETE.

  Args:
      url: The complete URL for the API request
      options: Dictionary of query parameters to add to the URL for filtering
      payload: Dictionary containing form data for the request body
      conn: Dictionary containing the credential configuration
      request_type: HTTP method type ("GET", "POST", "PUT", "PATCH", "DEL")
      json_payload: Dictionary containing JSON data for the request body

  Returns:
      dict: JSON response from the API

  Raises:
      requests.HTTPError: If the API request fails
      
  Examples:
      >>> response = request_json(
      ...     "https://api.servicetitan.io/jpm/v2/tenant/123/jobs",
      ...     options={"pageSize": 100},
      ...     conn=connection_config
      ... )
  """
  headers = get_auth_headers(conn)
  response = requests.request(request_type, url, data=payload, headers=headers, params=options, json=json_payload)
  if response.status_code != requests.codes.ok:
    logger.error(f"Error fetching data (url={url}, heads={headers}, data={payload}, json={json_payload}): {response.text}")
    response.raise_for_status()

  return response.json()

def check_default_options(options):
  """Add sensible defaults to options when not defined.
  
  Ensures that API request options have reasonable defaults to prevent
  issues with pagination and data retrieval.
  
  Args:
      options: Dictionary of request options/parameters
      
  Returns:
      dict: Options dictionary with defaults applied
      
  Examples:
      >>> options = check_default_options({})
      >>> # Returns: {"pageSize": 100}
      >>> options = check_default_options({"pageSize": 50})
      >>> # Returns: {"pageSize": 50} (unchanged)
  """
  # TODO: Add ability to read from a configuration file
  if "pageSize" not in options:
    options["pageSize"] = 100
  
  return options

def endpoint_url(folder, endpoint, id="", modifier="", conn=None, tenant_id=""):
  """Constructs API request URL based on key parameters.

  Builds the complete ServiceTitan API URL using the standard URL structure
  and allows for various endpoint configurations including specific IDs and modifiers.

  Args:
      folder: The API endpoint category/folder (e.g., "jpm", "sales", "inventory")
      endpoint: The specific endpoint within the folder (e.g., "jobs", "estimates")
      id: Optional specific record ID to append to the URL
      modifier: Optional additional path segment for specialized endpoints
      conn: Dictionary containing the credential configuration
      tenant_id: Optional manual override for the tenant ID

  Returns:
      str: Complete API URL ready for requests

  Raises:
      KeyError: If required connection information is missing
      
  Examples:
      >>> url = endpoint_url("jpm", "jobs", conn=conn)
      >>> # Returns: "https://api.servicetitan.io/jpm/v2/tenant/12345/jobs"
      
      >>> url = endpoint_url("jpm", "jobs", id="67890", modifier="notes", conn=conn)
      >>> # Returns: "https://api.servicetitan.io/jpm/v2/tenant/12345/jobs/67890/notes"
  """  
  # Adds ability to manually switch up the Tenant ID for apps that have multiples
  if tenant_id == "":
    tenant_id = get_tenant_id(conn)

  url = f"{conn['api_root']}/{folder}/v2/tenant/{tenant_id}/{endpoint}"
  if id != "": url = f"{url}/{id}"
  if modifier != "": url = f"{url}/{modifier}"
  return url
    
def create_credential_file(name="servicepytan_config.json"):
  """Creates and saves an unfilled configuration file template.

  Generates a JSON configuration file with empty credential fields that can be
  filled in with actual ServiceTitan API credentials.

  Args:
      name: Filename for the configuration file

  Returns:
      str: Path to the created configuration file
      
  Examples:
      >>> filepath = create_credential_file("my_config.json")
      >>> # Creates a file with empty credential template
  """  
  file = open(name, 'w')
  file.write(
    """{
    "SERVICETITAN_CLIENT_ID": "",
    "SERVICETITAN_CLIENT_SECRET": "",
    "SERVICETITAN_APP_ID": "",
    "SERVICETITAN_APP_KEY": "",
    "SERVICETITAN_TENANT_ID": ""
    }"""
  )
  file.close()
  return name

def get_timezone_by_file(conn=None):
  """Retrieves timezone from the connection configuration.

  Extracts the timezone setting from the connection configuration object,
  defaulting to "UTC" if no timezone is specified.

  Args:
      conn: Dictionary containing the credential configuration

  Returns:
      str: Timezone string (e.g., "America/New_York", "UTC")
      
  Examples:
      >>> tz = get_timezone_by_file(conn)
      >>> # Returns: "America/New_York" or "UTC" if not specified
  """    
  # Read File
  if conn and "SERVICETITAN_TIMEZONE" in conn:
    timezone = conn['SERVICETITAN_TIMEZONE']
  else:
    timezone = "UTC"
  return timezone

def sleep_with_countdown(sleep_time):
  """Sleeps for a given amount of time with a countdown display.
  
  Provides a visual countdown timer during sleep periods, typically used
  when handling rate limiting or waiting between API requests.
  
  Args:
      sleep_time: Number of seconds to sleep
      
  Examples:
      >>> sleep_with_countdown(30)
      >>> # Displays: "Trying again in 30 seconds...", "29 seconds...", etc.
  """
  for i in range(sleep_time, 0, -1):
      logger.info("Trying again in {} seconds...       ".format(i),end='\r')
      time.sleep(1)
  logger.info("")
  pass

def request_json_with_retry(url, options={}, payload="", conn=None, request_type="GET", json_payload=""):
  """Makes the request to the API and returns JSON with automatic retry for rate limits.

  Enhanced version of request_json that automatically handles rate limiting by
  detecting 429 status codes and retrying after the specified wait time.

  Args:
      url: The complete URL for the API request
      options: Dictionary of query parameters to add to the URL for filtering
      payload: Dictionary containing form data for the request body
      conn: Dictionary containing the credential configuration
      request_type: HTTP method type ("GET", "POST", "PUT", "PATCH", "DEL")
      json_payload: Dictionary containing JSON data for the request body

  Returns:
      dict: JSON response from the API

  Raises:
      requests.HTTPError: If the API request fails (non-rate-limit errors)
      
  Examples:
      >>> response = request_json_with_retry(
      ...     "https://api.servicetitan.io/jpm/v2/tenant/123/jobs",
      ...     options={"pageSize": 100},
      ...     conn=connection_config
      ... )
      >>> # Automatically retries if rate limited
  """
  response = request_json(url, options=options, payload=payload, conn=conn, request_type=request_type, json_payload=json_payload)
  if "traceId" in response:
    if response['status'] == 429:
        sleep_time = response['title'].split(" ")[-2]
        logger.warning("Rate Limit Exceeded. Retrying in {} seconds...".format(sleep_time))
        sleep_with_countdown(int(sleep_time))
        response = request_json_with_retry(url, options=options, payload=payload, conn=conn, request_type=request_type, json_payload=json_payload)
  
  return response

def request_contents(url, options={}, conn=None):
  """Fetches the contents of a URL with optional query parameters.

  Args:
      url: The complete URL for the API request
      options: Dictionary of query parameters to add to the URL
      conn: Dictionary containing the credential configuration

  Returns:
      dict: JSON response from the API

  Raises:
      requests.HTTPError: If the API request fails
  """
  response = requests.get(url, params=options, headers=get_auth_headers(conn))
  response.raise_for_status()
  
  if response.status_code != requests.codes.ok:
    logger.error(f"Error fetching contents (url={url}, options={options}): {response.text}")
    response.raise_for_status()

  return response.content