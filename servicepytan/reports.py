import math
from servicepytan.utils import request_json, get_timezone_by_file, endpoint_url, request_json_with_retry

class Report:
  """Primary class for retrieving Reporting Endpoint Data.

  Attributes:
      config_file: a string file path to the config file.
  """
  def __init__(self, category, report_id, config_file="servicepytan_config.json"):
    """Inits DataService with configuration file and authentication settings."""
    self.config_file = config_file
    self.timezone = get_timezone_by_file(config_file)
    self.category = category
    self.report_id = report_id

  def get_data(self, params, page=1, page_size=5000):
    """get report data"""
    options = {"page": page, "pageSize": page_size, "includeTotal": True}
    endpoint = f"report-category/{self.category}/reports/{self.report_id}/data"
    url = endpoint_url("reporting",endpoint, config_file=self.config_file)
    return request_json_with_retry(url, options=options, json_payload=params, 
              config_file=self.config_file, request_type="POST")
  
  def get_all_data(self, params, page_size=5000):
    """get all report data"""
    page = 1
    data = []
    fields = []
    response = self.get_data(params, page=page, page_size=page_size)
    data.extend(response["data"])
    fields.extend(response["fields"])
    total = response["totalCount"]
    requests_needed = math.ceil(total / page_size)
    mins_to_complete = requests_needed * 5
    if mins_to_complete > 60:
      print(f"This request will take at least {mins_to_complete/60} hours to complete.")
      print("Limit the parameters to reduce the number of requests and try again.")
      return {"error": "Too many requests. Try again with fewer parameters."}
    while len(data) < total:
      page += 1
      response = self.get_data(params, page=page, page_size=page_size)
      data.extend(response["data"])
    return {"data": data, "fields": fields}