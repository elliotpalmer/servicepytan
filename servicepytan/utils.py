"""Utility Functions for Supporting Other Modules"""
import requests
import time
from servicepytan.auth import get_auth_headers, get_tenant_id

def request_json(url, options={}, payload={}, conn=None, request_type="GET", json_payload={}):
  """Makes the request to the API and returns JSON

  Retrieves JSON response from provided URL with a number of parameters to customize the request.

  Args:
      url: A string with the full URL request
      options: A dictionary defining the parameters to add to the url for filtering
      payload: A dictionary defining the data object to create or update
      conn: a dictionary containing the credential config.
      request_type: A string to define the REST endpoint type [GET, POST, PUT, PATCH, DEL].

  Returns:
      JSON Object

  Raises:
      TBD
  """
  headers = get_auth_headers(conn)
  response = requests.request(request_type, url, data=payload, headers=headers, params=options, json=json_payload)
  if response.status_code != requests.codes.ok:
    print(f"Error fetching data (url={url}, heads={headers}, data={payload}, json={json_payload}): {response.text}")
    response.raise_for_status()

  return response.json()

def check_default_options(options):
  """Add sensible defaults to options when not defined"""
  # TODO: Add ability to read from a configuration file
  if "pageSize" not in options:
    options["pageSize"] = 100
  
  return options

def endpoint_url(folder, endpoint, id="", modifier="", conn=None, tenant_id=""):
  """Constructs API request URL based on key parameters

  Retrives JSON response from provided URL with a number of parameters to customize the request.

  Args:
      folder: A string based on the endpoint groupings
      endpoint: A string indicating the endpoint you want to address.
      id: A string for the id of the endpoint object you're addressing.
      modifier: A string to modify the url to address the additional endpoint.
      conn: a dictionary containing the credential config.
      tenant_id: A string to manually adjust the tenant id.

  Returns:
      A URL String

  Raises:
      TBD
  """  
  # Adds ability to manually switch up the Tenant ID for apps that have multiples
  if tenant_id == "":
    tenant_id = get_tenant_id(conn)

  url = f"{conn['api_root']}/{folder}/v2/tenant/{tenant_id}/{endpoint}"
  if id != "": url = f"{url}/{id}"
  if modifier != "": url = f"{url}/{modifier}"
  return url
    
def create_credential_file(name="servicepytan_config.json"):
  """Creates and saves an unfilled configuration file.

  Args:
      name: a dictionary containing the credential config

  Returns:
      A filepath string
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
  """Retrieves timezone from the configuration file.

  Args:
      conn: a dictionary containing the credential config

  Returns:
      Timezone string
  """    
  # Read File
  if "SERVICETITAN_TIMEZONE" in conn:
    timezone = config['SERVICETITAN_TIMEZONE']
  else:
    timezone = "UTC"
  return timezone

def sleep_with_countdown(sleep_time):
  """Sleeps for a given amount of time with a countdown"""
  for i in range(sleep_time, 0, -1):
      print("Trying again in {} seconds...       ".format(i),end='\r')
      time.sleep(1)
  print("")
  pass

def request_json_with_retry(url, options={}, payload="", conn=None, request_type="GET", json_payload=""):
  """Makes the request to the API and returns JSON with a retry

  Retrieves JSON response from provided URL with a number of parameters to customize the request.

  Args:
      url: A string with the full URL request
      options: A dictionary defining the parameters to add to the url for filtering
      payload: A dictionary defining the data object to create or update
      conn: a dictionary containing the credential config.
      request_type: A string to define the REST endpoint type [GET, POST, PUT, PATCH, DEL].
      retry_count: An integer for the number of times to retry the request.
      sleep_time: An integer for the number of seconds to sleep between retries.

  Returns:
      JSON Object

  Raises:
      TBD
  """
  response = request_json(url, options=options, payload=payload, conn=conn, request_type=request_type, json_payload=json_payload)
  if "traceId" in response:
    if response['status'] == 429:
        sleep_time = response['title'].split(" ")[-2]
        print("Rate Limit Exceeded. Retrying in {} seconds...".format(sleep_time))
        sleep_with_countdown(int(sleep_time))
        response = request_json_with_retry(url, options=options, payload=payload, conn=conn, request_type=request_type, json_payload=json_payload)
  
  return response