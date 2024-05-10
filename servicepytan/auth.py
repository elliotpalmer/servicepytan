"""Authenticating with ServiceTitan API"""

import requests
import json
import os
from dotenv import load_dotenv
from enum import StrEnum

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


class ApiEnvironment(StrEnum):
    PRODUCTION  = "production",
    INTEGRATION = "integration"

def get_auth_root_url(env: str) -> str:
    match env:
        case ApiEnvironment.PRODUCTION:
            return "https://auth.servicetitan.io"
        case ApiEnvironment.INTEGRATION:
            return "https://auth-integration.servicetitan.io"
        case _:
            raise ValueError(f"Unknown ApiEnvironment: {env}")

def get_api_root_url(env: str) -> str:
    match env:
        case ApiEnvironment.PRODUCTION:
            return "https://api.servicetitan.io"
        case ApiEnvironment.INTEGRATION:
            return "https://api-integration.servicetitan.io"
        case _:
            raise ValueError(f"Unknown ApiEnvironment: {env}")


AUTH_VARIABLES = [
    'SERVICETITAN_APP_KEY',
    'SERVICETITAN_TENANT_ID',
    'SERVICETITAN_CLIENT_ID',
    'SERVICETITAN_CLIENT_SECRET',
    'SERVICETITAN_APP_ID',
    'SERVICETITAN_TIMEZONE',

    'SERVICETITAN_API_ENVIRONMENT'  # One of values of the ApiEnvironment enum
]

def servicepytan_connect(
    api_environment: str,
    app_key:str=None, tenant_id:str=None, client_id:str=None, 
    client_secret:str=None, app_id:str=None, timezone:str="UTC", config_file:str=None):
    
    auth_config_object = {
        "SERVICETITAN_APP_KEY": app_key,
        "SERVICETITAN_TENANT_ID": tenant_id,
        "SERVICETITAN_CLIENT_ID": client_id,
        "SERVICETITAN_CLIENT_SECRET": client_secret,
        "SERVICETITAN_APP_ID": app_id,
        "SERVICETITAN_TIMEZONE": timezone,

        'SERVICETITAN_API_ENVIRONMENT': api_environment,

        "auth_root": get_auth_root_url(api_environment),
        "api_root": get_api_root_url(api_environment),
    }


    # First check if the config_file is provided
    if config_file:
        logger.info("Setting auth config from file...")
        f = open(config_file)
        creds = json.load(f)
        for var in AUTH_VARIABLES:
            auth_config_object[var] = creds.get(var, '')
        f.close()

    # If not, check if the environment variables are set
    # AFAICT, app_id is never used in the rest of the code, so it isn't necessary
    elif not api_environment or not app_key or not tenant_id or not client_id or not client_secret:
        load_dotenv()
        logger.info("Auth config not provided, loading from environment variables...")
        for var in AUTH_VARIABLES:
            auth_var = os.environ.get(var)
            if auth_var:
                auth_config_object[var] = auth_var
            else:
                logger.info(f"Environment variable {var} not found or provided in function. Defaulting to empty string.")
                auth_config_object[var] = ''

    return auth_config_object

def request_auth_token(auth_root_url: str, client_id, client_secret):
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

  url: str = f"{auth_root_url}/connect/token"

  headers: dict = {
    "Content-Type": "application/x-www-form-urlencoded",
  }
  data: dict = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
  }

  response = requests.post(url, headers=headers, data=data)
  if response.status_code != requests.codes.ok:
    logger.error(f"Error fetching auth token (url={url}, header={headers}, data={data}): {response.text}")
    response.raise_for_status()

  return response.json()

def get_auth_token(conn):
  """Fetches Auth Token using the config_file.

  Retrives the CLIENT_ID and CLIENT_SECRET entries from config_file.

  Args:
      config_file: String, path to the config file defaults to 'servicepytan_config.json'

  Returns:
      Authentication token

  Raises:
      TBD
  """
  # Read File
  client_id = conn['SERVICETITAN_CLIENT_ID']
  client_secret = conn['SERVICETITAN_CLIENT_SECRET']
  return request_auth_token(conn["auth_root"], client_id, client_secret)["access_token"]

def get_app_key(conn):
  """Fetches App Key from the config_file.

  Retrives the APP_KEY entry from config_file.

  Args:
      config_file: String, path to the config file defaults to 'servicepytan_config.json'

  Returns:
      App Key

  Raises:
      TBD
  """
  app_key = conn['SERVICETITAN_APP_KEY']
  return app_key

def get_tenant_id(conn):
  """Fetches Tenant ID from the config_file.

  Retrives the TENANT_ID entry from config_file.

  Args:
      config_file: String, path to the config file defaults to 'servicepytan_config.json'

  Returns:
      Tenant ID

  Raises:
      TBD
  """
  tenant_id = conn['SERVICETITAN_TENANT_ID']
  return tenant_id 

def get_auth_headers(conn):
  """Generates the Authentication Headers for each API request

  Creates an object that includes the auth token and app key formatted to create the auth headers.

  Args:
      config_file: String, path to the config file defaults to 'servicepytan_config.json'

  Returns:
      Object

  Raises:
      TBD
  """
  return {
      "Authorization": get_auth_token(conn),
      "ST-App-Key": get_app_key(conn)
  }