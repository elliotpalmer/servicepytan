from servicepytan.utils import request_json, check_default_options, endpoint_url
class Endpoint:
  """Primary class for interacting with the API by establishing an endpoint object.

  The core way of getting and changing data in ServiceTitan using the library is to create
  an endpoint object. Each method pulls the data in a different way and may or may not apply 
  to a certain endpoint. You will need to consult the developer docs to identify the exact
  parameters needed for a given endpoint and which methods will apply.

  Attributes:
      folder: A string indicating the group of endpoints you want to address.
      endpoint: A string indicating the endpoint you want to address.
      config_file: a string file path to the config file.
  """
  def __init__(self, folder, endpoint, config_file='servicepytan_config.json'):
    """Inits Endpoint with folder, endpoint and allows for getting necessary credentials from the config file."""
    self.folder = folder
    self.endpoint = endpoint
    self.config_file = config_file

  # Main Request Types
  def get_one(self, id, modifier=""):
    """Retrieve one record using the record id. Modifier is used for further endpoints."""
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=modifier, config_file=self.config_file)
    return request_json(url, options={}, payload="", config_file=self.config_file, request_type="GET")

  def get_many(self, query={}):
    """Retrieve one page of results with query options to customize."""
    url = endpoint_url(self.folder, self.endpoint, config_file=self.config_file)
    options = check_default_options(query)
    return request_json(url, options, payload="", config_file=self.config_file, request_type="GET")
  
  def get_all(self, query={}):
    """Retrive all pages in your query."""
    query["page"] = "1"
    print(query)
    response = self.get_many(query)
    data = response["data"]
    if data == []: return []
    has_more = response["hasMore"]
    while has_more:
      query["page"] = str(int(query["page"]) + 1)
      print(query)
      response = self.get_many(query)
      data.extend(response["data"])
      has_more = response["hasMore"]

    return data

  def create(self, payload):
    """Method that corresponds to a POST request for creating objects"""
    url = endpoint_url(self.folder, self.endpoint, config_file=self.config_file)
    return request_json(url, options={}, payload=payload, config_file=self.config_file, request_type="POST")

  def update(self, id, payload, modifier="", request_type="PUT"):
    """Method that corresponds to PUT or POST request for updating objects. Defaults to PUT"""
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=modifier, config_file=self.config_file)
    return request_json(url, options={}, payload=payload, config_file=self.config_file, request_type=request_type)

  def delete(self, id, modifier=""):
    """Method that corresponds to a DEL request for deleting objects"""
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=f"{modifier}", config_file=self.config_file)
    return request_json(url, options={}, payload="", config_file=self.config_file, request_type="DEL")

  def delete_subitem(self, id, modifier_id, modifier):
    """Method that corresponds to a DEL request for deleting objects with subitems"""
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=f"{modifier}/{modifier_id}", config_file=self.config_file)
    return request_json(url, options={}, payload="", config_file=self.config_file, request_type="DEL")