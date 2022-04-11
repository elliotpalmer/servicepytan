"""Authenticating with ServiceTitan API"""

import requests
import json
from servicepytan import URL_ROOT, AUTH_ROOT

def get_auth_token(client_id, client_secret):
  """Fetches Auth Token.

  Retrieves authentication token for completing a request against the API

  Args:
      client_id: String, provided from the integration settings
      client_secret: String, provided from the integration settings

  Returns:
      Authentication token

  Raises:
      TBD
  """

  url = f"{AUTH_ROOT}/connect/token"

  querystring = {"Content-Type":"application/x-www-form-urlencoded"}

  payload = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
  headers = {"Content-Type": "application/x-www-form-urlencoded"}

  response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

  return json.loads(response.text)

def get_auth_token_by_file(config_file='servicepytan_config.json'):
  """Fetches Auth Token using the config_file.

  Retrives the CLIENT_ID and CLIENT_SECRET entries in config_file.

  Args:
      config_file: String, path to the config file defaults to 'servicepytan_config.json'

  Returns:
      Authentication token

  Raises:
      TBD
  """
  # Read File
  f = open(config_file)
  creds = json.load(f)
  client_id = creds['CLIENT_ID']
  client_secret = creds['CLIENT_SECRET']
  f.close()
  return get_auth_token(client_id, client_secret)["access_token"]

def get_app_key(config_file='servicepytan_config.json'):
  f = open(config_file)
  creds = json.load(f)
  app_key = creds['APP_KEY']
  f.close()
  return app_key

def get_tenant_id(config_file='servicepytan_config.json'):
  f = open(config_file)
  creds = json.load(f)
  tenant_id = creds['TENANT_ID']
  f.close()
  return tenant_id 

def get_auth_headers(config_file='servicepytan_config.json'):
   return {
      "Authorization": get_auth_token_by_file(config_file),
      "ST-App-Key": get_app_key(config_file)
  }