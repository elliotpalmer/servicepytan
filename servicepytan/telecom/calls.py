from servicepytan.auth import get_tenant_id
from servicepytan.utils import request_json, check_default_options, endpoint_url, get_folder_and_path

folder, endpoint = get_folder_and_path()

def get_by_id(id, options={}, modifier="", key_file='st_api_credentials.json', request_type="GET"):
  url = endpoint_url(folder, endpoint, id=id, modifier=modifier, key_file=key_file)
  options = check_default_options(options)
  return request_json(url, options, payload="", key_file=key_file, request_type=request_type)

def get_list(options={}, key_file='st_api_credentials.json', request_type="GET"):
  url = endpoint_url(folder, endpoint, key_file=key_file)
  options = check_default_options(options)
  return request_json(url, options, payload="", key_file=key_file, request_type=request_type)

def update(id, payload, options={}, key_file='st_api_credentials.json', request_type="PUT"):
  url = endpoint_url(folder, endpoint, id=id, modifier=modifier, key_file=key_file)
  options = check_default_options(options)
  return request_json(url, options, payload="", key_file=key_file, request_type=request_type)

def create():
  pass

def delete():
  pass