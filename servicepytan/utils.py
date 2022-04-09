import requests
import json
import inspect
from servicepytan import URL_ROOT, AUTH_ROOT
from servicepytan.auth import get_auth_headers, get_tenant_id

def request_json(url, options={}, payload="", config_file='servicepytan_config.json', request_type="GET"):
  headers = get_auth_headers(config_file)
  response = requests.request(request_type, url, data=payload, headers=headers, params=options)
  return json.loads(response.text)

def check_default_options(options):
  # TODO: Add ability to read from a configuration file
  if "pageSize" not in options:
    options["pageSize"] = 100
  
  return options

def endpoint_url(folder, endpoint, id="", modifier="", config_file='servicepytan_config.json', tenant_id=""):
  
  # Adds ability to manually switch up the Tenant ID for apps that have multiples
  if tenant_id == "":
    tenant_id = get_tenant_id(config_file)

  url = f"{URL_ROOT}/{folder}/v2/tenant/{tenant_id}/{endpoint}"
  if id != "": url = f"{url}/{id}"
  if modifier != "": url = f"{url}/{modifier}"
  return url

def get_folder_and_path():
  stack = inspect.stack()
  filename = stack[1].filename
  file = filename.split("/")
  endpoint = file[-1].replace(".py","")
  folder = file[-2]
  return folder, endpoint
    
def create_credential_file(name="servicepytan_config.json"):

  file = open(name, 'w')
  file.write(
    """
    {
      "CLIENT_ID": "",
      "CLIENT_SECRET": "",
      "APP_ID": "",
      "APP_KEY": "",
      "TENANT_ID": ""
    }
    """
  )
  file.close()
  return name

def get_timezone_by_file(config_file='servicepytan_config.json'):
  # Read File
  f = open(config_file)
  config = json.load(f)
  if "TIMEZONE" in config:
    timezone = config['TIMEZONE']
  else:
    timezone = ""
  f.close()
  return timezone