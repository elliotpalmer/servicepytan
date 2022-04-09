from servicepytan.utils import request_json, check_default_options, endpoint_url, get_folder_and_path

# folder, endpoint = get_folder_and_path()
class Endpoint:
  def __init__(self, folder, endpoint, config_file='servicepytan_config.json'):
    self.folder = folder
    self.endpoint = endpoint
    self.config_file = config_file

  # Main Request Types
  def get_one(self, id, modifier=""):
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=modifier, config_file=self.config_file)
    return request_json(url, options={}, payload="", config_file=self.config_file, request_type="GET")

  def get_many(self, query={}):
    url = endpoint_url(self.folder, self.endpoint, config_file=self.config_file)
    options = check_default_options(query)
    return request_json(url, options, payload="", config_file=self.config_file, request_type="GET")
  
  def get_all(self, query={}):
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
    url = endpoint_url(self.folder, self.endpoint, config_file=self.config_file)
    return request_json(url, options={}, payload=payload, config_file=self.config_file, request_type="POST")

  def update(self, id, payload, modifier="", request_type="PUT"):
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=modifier, config_file=self.config_file)
    return request_json(url, options={}, payload=payload, config_file=self.config_file, request_type=request_type)

  def delete(id, modifier=""):
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=f"{modifier}", config_file=self.config_file)
    return request_json(url, options={}, payload="", config_file=self.config_file, request_type="DEL")

  def delete_subitem(id, modifier_id, modifier):
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=f"{modifier}/{modifier_id}", config_file=self.config_file)
    return request_json(url, options={}, payload="", config_file=self.config_file, request_type="DEL")