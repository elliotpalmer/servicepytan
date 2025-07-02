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
    """Enumeration for ServiceTitan API environments.
    
    This enum defines the available API environments for ServiceTitan,
    allowing users to switch between production and integration environments.
    
    Attributes:
        PRODUCTION: Production environment for live data
        INTEGRATION: Integration environment for testing
    """
    PRODUCTION  = "production",
    INTEGRATION = "integration"

def get_auth_root_url(env: str) -> str:
    """Get the authentication root URL for the specified environment.
    
    Args:
        env: The API environment (production or integration)
        
    Returns:
        str: The authentication root URL for the specified environment
        
    Raises:
        ValueError: If the environment is not recognized
        
    Examples:
        >>> get_auth_root_url(ApiEnvironment.PRODUCTION)
        'https://auth.servicetitan.io'
        >>> get_auth_root_url(ApiEnvironment.INTEGRATION)
        'https://auth-integration.servicetitan.io'
    """
    match env:
        case ApiEnvironment.PRODUCTION:
            return "https://auth.servicetitan.io"
        case ApiEnvironment.INTEGRATION:
            return "https://auth-integration.servicetitan.io"
        case _:
            raise ValueError(f"Unknown ApiEnvironment: {env}")

def get_api_root_url(env: str) -> str:
    """Get the API root URL for the specified environment.
    
    Args:
        env: The API environment (production or integration)
        
    Returns:
        str: The API root URL for the specified environment
        
    Raises:
        ValueError: If the environment is not recognized
        
    Examples:
        >>> get_api_root_url(ApiEnvironment.PRODUCTION)
        'https://api.servicetitan.io'
        >>> get_api_root_url(ApiEnvironment.INTEGRATION)
        'https://api-integration.servicetitan.io'
    """
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
    api_environment: str=ApiEnvironment.production,
    app_key:str=None, tenant_id:str=None, client_id:str=None, 
    client_secret:str=None, app_id:str=None, timezone:str="UTC", config_file:str=None):
    """Establish connection configuration for ServiceTitan API.
    
    This function creates a configuration object with all necessary credentials
    and settings for connecting to the ServiceTitan API. It can source credentials
    from function parameters, a config file, or environment variables.
    
    Args:
        api_environment: The API environment to use (production or integration)
        app_key: ServiceTitan application key
        tenant_id: ServiceTitan tenant identifier
        client_id: OAuth client ID for authentication
        client_secret: OAuth client secret for authentication
        app_id: ServiceTitan application ID (optional)
        timezone: Timezone for date operations (defaults to "UTC")
        config_file: Path to JSON configuration file containing credentials
        
    Returns:
        dict: Configuration object containing all necessary authentication settings
        
    Examples:
        >>> # Using parameters
        >>> conn = servicepytan_connect(
        ...     api_environment="production",
        ...     app_key="your_app_key",
        ...     tenant_id="your_tenant_id",
        ...     client_id="your_client_id",
        ...     client_secret="your_client_secret"
        ... )
        
        >>> # Using config file
        >>> conn = servicepytan_connect(config_file="credentials.json")
        
        >>> # Using environment variables (will auto-load from .env)
        >>> conn = servicepytan_connect()
    """
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
  """Fetches Auth Token using the connection configuration.

  Retrieves the CLIENT_ID and CLIENT_SECRET entries from the connection object
  and requests an authentication token from the ServiceTitan API.

  Args:
      conn: Dictionary containing the credential configuration

  Returns:
      str: Authentication token

  Raises:
      requests.HTTPError: If the authentication request fails
  """
  # Read File
  client_id = conn['SERVICETITAN_CLIENT_ID']
  client_secret = conn['SERVICETITAN_CLIENT_SECRET']
  return request_auth_token(conn["auth_root"], client_id, client_secret)["access_token"]

def get_app_key(conn):
  """Fetches App Key from the connection configuration.

  Retrieves the APP_KEY entry from the connection object.

  Args:
      conn: Dictionary containing the credential configuration

  Returns:
      str: ServiceTitan App Key

  Raises:
      KeyError: If the APP_KEY is not found in the connection configuration
  """
  app_key = conn['SERVICETITAN_APP_KEY']
  return app_key

def get_tenant_id(conn):
  """Fetches Tenant ID from the connection configuration.

  Retrieves the TENANT_ID entry from the connection object.

  Args:
      conn: Dictionary containing the credential configuration

  Returns:
      str: ServiceTitan Tenant ID

  Raises:
      KeyError: If the TENANT_ID is not found in the connection configuration
  """
  tenant_id = conn['SERVICETITAN_TENANT_ID']
  return tenant_id 

def get_auth_headers(conn):
  """Generates the Authentication Headers for each API request.

  Creates a dictionary that includes the auth token and app key formatted 
  to create the authentication headers required by the ServiceTitan API.

  Args:
      conn: Dictionary containing the credential configuration

  Returns:
      dict: Dictionary containing Authorization and ST-App-Key headers

  Raises:
      requests.HTTPError: If authentication token retrieval fails
      KeyError: If required credentials are missing
      
  Examples:
      >>> headers = get_auth_headers(conn)
      >>> # headers = {
      >>> #     "Authorization": "Bearer your_token_here",
      >>> #     "ST-App-Key": "your_app_key_here"
      >>> # }
  """
  return {
      "Authorization": get_auth_token(conn),
      "ST-App-Key": get_app_key(conn)
  }