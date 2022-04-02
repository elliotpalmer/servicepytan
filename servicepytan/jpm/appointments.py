# import requests
# import json

from servicepytan.auth import get_tenant_id
from servicepytan.utils import request_json, check_default_options
from servicepytan.jpm import BASE_URL

def set_url(key_file='st_api_credentials.json'): return f"{BASE_URL}/{get_tenant_id(key_file)}/appointments"

def get_appointments_by_id(appointment_id, options={}, key_file='st_api_credentials.json', request_type="GET"):
  url = f"{set_url(key_file)}/{appointment_id}"
  options = check_default_options(options)
  return request_json(url, options, payload="", key_file=key_file, request_type=request_type)

def get_appointments(options={}, key_file='st_api_credentials.json', request_type="GET"):
  url = f"{set_url(key_file)}"
  return request_json(url, options, payload="", key_file=key_file, request_type=request_type)

def create_appointments(appointments, key_file='st_api_credentials.json'):
  pass