from servicepytan.utils import request_json, get_timezone_by_file, endpoint_url

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

  def get_data(self, params):
    """get report data"""
    url = endpoint_url("reporting",f"report-category/{self.category}/reports/{self.report_id}/data", config_file=self.config_file)
    return request_json(url, json_payload=params, config_file=self.config_file, request_type="POST")