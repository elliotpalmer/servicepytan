from servicepytan.utils import request_json, check_default_options, endpoint_url, get_folder_and_path

# folder, endpoint = get_folder_and_path()
class Endpoint:
  def __init__(self, folder, endpoint, key_file='st_api_credentials.json'):
    self.folder = folder
    self.endpoint = endpoint
    self.key_file = key_file

  # Main Request Types
  def get_one(self, id, modifier=""):
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=modifier, key_file=self.key_file)
    # options = check_default_options(query)
    return request_json(url, options={}, payload="", key_file=self.key_file, request_type="GET")

  def get_many(self, query={}):
    url = endpoint_url(self.folder, self.endpoint, key_file=self.key_file)
    options = check_default_options(query)
    return request_json(url, options, payload="", key_file=self.key_file, request_type="GET")
  
  def get_all(self, query={}):
    query["page"] = "1"
    print(query)
    response = self.get_many(query)
    data = response["data"]
    has_more = response["hasMore"]
    while has_more:
      query["page"] = str(int(query["page"]) + 1)
      print(query)
      response = self.get_many(query)
      data.extend(response["data"])
      has_more = response["hasMore"]

    return data

  def create(self, payload):
    url = endpoint_url(self.folder, self.endpoint, key_file=self.key_file)
    return request_json(url, options={}, payload=payload, key_file=self.key_file, request_type="POST")

  def update(self, id, payload, modifier="", request_type="PUT"):
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=modifier, key_file=self.key_file)
    return request_json(url, options={}, payload=payload, key_file=self.key_file, request_type=request_type)

  def delete(id, modifier=""):
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=f"{modifier}", key_file=self.key_file)
    return request_json(url, options={}, payload="", key_file=self.key_file, request_type="DEL")

  def delete_subitem(id, modifier_id, modifier):
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=f"{modifier}/{modifier_id}", key_file=self.key_file)
    return request_json(url, options={}, payload="", key_file=self.key_file, request_type="DEL")