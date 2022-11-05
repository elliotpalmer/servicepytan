import math
from servicepytan.utils import request_json, get_timezone_by_file, endpoint_url, request_json_with_retry

def get_report_categories(config_file="servicepytan_config.json"):
    """Get a list of report categories"""
    return request_json(endpoint_url('reporting', 'report-categories', config_file=config_file), config_file=config_file)

def get_report_list(report_category, config_file="servicepytan_config.json"):
    """Get a list of reports for a given report category"""
    return request_json(endpoint_url('reporting', f'report-category/{report_category}/reports', config_file=config_file), config_file=config_file)

def get_dynamic_set_list(dynamic_set_id,config_file="servicepytan_config.json"):
    """Get a list of dynamic sets"""
    return request_json(endpoint_url('reporting', f'dynamic-value-sets/{dynamic_set_id}', config_file=config_file), config_file=config_file)

class Report:
  """Primary class for retrieving Reporting Endpoint Data.

  Attributes:
      category: A string representing the report category. Find list of categories with get_report_categories().
      report_id: A string representing the report id. Find list of report_id using get_report_list().
      config_file: a string file path to the config file.
  """
  def __init__(self, category, report_id, config_file="servicepytan_config.json"):
    """Inits DataService with configuration file and authentication settings."""
    self.config_file = config_file
    self.timezone = get_timezone_by_file(config_file)
    self.category = category
    self.report_id = report_id
    self.params = {"parameters": []}
    self.metadata = self.get_metadata()

  def add_params(self, name, value):
    """add a parameter to the report"""
    param_keys = [param["name"] for param in self.params["parameters"]]
    if name in param_keys:
      print(f"Parameter '{name}' already exists. Updating value from '{self.params['parameters'][param_keys.index(name)]['value']}' to '{value}'...")
      self.update_params(name, value)
    else:
      self.params["parameters"].append({"name": name, "value": value})

  def update_params(self, name, value):
    """update a parameter in the report"""
    param_keys = [param["name"] for param in self.params["parameters"]]
    if name in param_keys:
      self.params["parameters"][param_keys.index(name)]["value"] = value
    else:
      print(f"Parameter '{name}' does not exist. Adding parameter...")
      self.add_params(name, value)

  def get_params(self):
    """get report parameters"""
    return self.params

  def get_metadata(self):
    """get report metadata"""
    endpoint = f"report-category/{self.category}/reports/{self.report_id}"
    url = endpoint_url("reporting",endpoint, config_file=self.config_file)
    return request_json_with_retry(url, config_file=self.config_file)

  def show_param_types(self):
    """show parameter types"""
    for param in self.metadata["parameters"]:
      dynamic_set_id = ""
      required = "[ ]"
      if param["isRequired"]:
        required = "[*]"
      if param['acceptValues']:
        dynamic_set_id = f" (dynamicSetId: {param['acceptValues']['dynamicSetId']})"
      print(f"{required} - {param['name']}: {param['dataType']}, {dynamic_set_id}")

  def get_data(self, params="", page=1, page_size=5000):
    """get report data"""
    if params == "":
      params = self.params
    options = {"page": page, "pageSize": page_size, "includeTotal": True}
    endpoint = f"report-category/{self.category}/reports/{self.report_id}/data"
    url = endpoint_url("reporting",endpoint, config_file=self.config_file)
    return request_json_with_retry(url, options=options, json_payload=params, 
              config_file=self.config_file, request_type="POST")
  
  def get_all_data(self, params="", page_size=5000):
    """get all report data"""
    page = 1
    data = []
    fields = []
    if params == "":
      params = self.params
    print("Getting first page of data...")
    response = self.get_data(params, page=page, page_size=page_size)
    data.extend(response["data"])
    fields.extend(response["fields"])
    total = response["totalCount"]
    has_more = response["hasMore"]
    print(f"Retrieved {len(data)} of {total} records...")
    requests_needed = math.ceil(total / page_size)
    mins_to_complete = requests_needed * 5
    updated_page_size = page_size
    if mins_to_complete > 60 or requests_needed > 2:
      init_page_size = updated_page_size
      if page_size < 5000 and math.ceil(total / 5000) < 12:
        print("Setting page size to 5000 to speed up report retrieval...")
        updated_page_size = 5000
        requests_needed = 1 + math.ceil((total - init_page_size) / updated_page_size)
      else:
        print(f"This request will take at least {mins_to_complete/60} hours to complete.")
        print("Limit the parameters to reduce the number of requests and try again.")
        return {"error": "Too many requests. Try again with fewer parameters."}
    while has_more:
      page += 1
      print(f"Getting page {page} of {requests_needed}...")
      response = self.get_data(params, page=page, page_size=updated_page_size)
      if(len(response["data"]) == 0):
        print("No more data to retrieve.")
        break
      data.extend(response["data"])
      print(f"Retrieved {len(data)} sof {total} records...")
      has_more = response["hasMore"]
    return {"data": data, "fields": fields}