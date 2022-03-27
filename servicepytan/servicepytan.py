"""Main module."""
import requests
URL_ROOT = https://auth.servicetitan.io

def get_auth_token(client_id, client_secret):
  """
  Method for authorizing with ServiceTitan API
  """

  url = f"{URL_ROOT}/connect/token"

  querystring = {"Content-Type":"application/x-www-form-urlencoded"}

  payload = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
  headers = {"Content-Type": "application/x-www-form-urlencoded"}

  response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

  return response.text

def get_app_key(key_file='st_api_credentials.json'):
  return "ak1.ojrmbys3ve1lsaj6gz4arkfx3"

def get_job_by_id(job_id, options):
  url = f"{URL_ROOT}/jpm/v2/tenant/{job_id}/jobs"

  # options = {"pageSize":"500","active":"any","completedOnOrAfter":"2022-03-14T00:00:00Z","page":"1","createdOnOrAfter":"2021-06-01T00:00:00Z"}

  payload = ""
  headers = {
      "Authorization": get_auth_token(),
      "ST-App-Key": get_app_key()
  }

  response = requests.request("GET", url, data=payload, headers=headers, params=options)

  print(response.text)