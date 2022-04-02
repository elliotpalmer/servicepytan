import requests
import json
import inspect
from servicepytan import URL_ROOT, AUTH_ROOT
from servicepytan.auth import get_auth_headers, get_tenant_id

def request_json(url, options={}, payload="", key_file='st_api_credentials.json', request_type="GET"):
  headers = get_auth_headers(key_file)
  response = requests.request(request_type, url, data=payload, headers=headers, params=options)
  return json.loads(response.text)

def check_default_options(options):
  # TODO: Add ability to read from a configuration file
  if "pageSize" not in options:
    options["pageSize"] = 100
  
  return options

def endpoint_url(folder, endpoint, id="", modifier="", key_file='st_api_credentials.json'):
  url = f"{URL_ROOT}/{folder}/v2/tenant/{get_tenant_id(key_file)}/{endpoint}"
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
    