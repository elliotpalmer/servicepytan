"""Main module."""
import requests
import json
from servicepytan import URL_ROOT, AUTH_ROOT

def test():
  return URL_ROOT

def get_auth_token(client_id, client_secret):
  """
  Method for authorizing with ServiceTitan API
  """

  url = f"{AUTH_ROOT}/connect/token"

  querystring = {"Content-Type":"application/x-www-form-urlencoded"}

  payload = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
  headers = {"Content-Type": "application/x-www-form-urlencoded"}

  response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

  return json.loads(response.text)

def get_auth_token_by_file(key_file='st_api_credentials.json'):
  # Read File
  f = open(key_file)
  creds = json.load(f)
  client_id = creds['CLIENT_ID']
  client_secret = creds['CLIENT_SECRET']
  f.close()
  return get_auth_token(client_id, client_secret)["access_token"]

def get_app_key(key_file='st_api_credentials.json'):
  f = open(key_file)
  creds = json.load(f)
  app_key = creds['APP_KEY']
  f.close()
  return app_key

def get_tenant_id(key_file='st_api_credentials.json'):
  f = open(key_file)
  creds = json.load(f)
  tenant_id = creds['TENANT_ID']
  f.close()
  return tenant_id 

def get_auth_headers(key_file='st_api_credentials.json'):
   return {
      "Authorization": get_auth_token_by_file(key_file),
      "ST-App-Key": get_app_key(key_file)
  }

def get_job_by_id(job_id, options={"pageSize": "100"}, key_file='st_api_credentials.json'):
  url = f"{URL_ROOT}/jpm/v2/tenant/{get_tenant_id(key_file)}/jobs/{job_id}"
  # options = {"pageSize":"500","active":"any","completedOnOrAfter":"2022-03-14T00:00:00Z","page":"1","createdOnOrAfter":"2021-06-01T00:00:00Z"}
  payload = ""
  headers = get_auth_headers(key_file)
  response = requests.request("GET", url, data=payload, headers=headers, params=options)
  return json.loads(response.text)