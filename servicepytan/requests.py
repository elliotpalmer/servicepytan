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
      conn: a dictionary containing the credential config.
  """
  def __init__(self, folder, endpoint, conn=None):
    """Inits Endpoint with folder, endpoint and allows for getting necessary credentials from the config file."""
    self.folder = folder
    self.endpoint = endpoint
    self.conn = conn

  # Main Request Types
  def get_one(self, id, modifier=""):
    """Retrieve one record using the record id. Modifier is used for further endpoints."""
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=modifier, conn=self.conn)
    return request_json(url, options={}, payload="", conn=self.conn, request_type="GET")

  def get_many(self, query={}):
    """Retrieve one page of results with query options to customize."""
    url = endpoint_url(self.folder, self.endpoint, conn=self.conn)
    options = check_default_options(query)
    return request_json(url, options, payload="", conn=self.conn, request_type="GET")
  
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
    url = endpoint_url(self.folder, self.endpoint, conn=self.conn)
    return request_json(url, options={}, payload=payload, conn=self.conn, request_type="POST")

  def update(self, id, payload, modifier="", request_type="PUT"):
    """Method that corresponds to PUT or POST request for updating objects. Defaults to PUT"""
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=modifier, conn=self.conn)
    return request_json(url, options={}, payload=payload, conn=self.conn, request_type=request_type)

  def delete(self, id, modifier=""):
    """Method that corresponds to a DEL request for deleting objects"""
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=f"{modifier}", conn=self.conn)
    return request_json(url, options={}, payload="", conn=self.conn, request_type="DEL")

  def delete_subitem(self, id, modifier_id, modifier):
    """Method that corresponds to a DEL request for deleting objects with subitems"""
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=f"{modifier}/{modifier_id}", conn=self.conn)
    return request_json(url, options={}, payload="", conn=self.conn, request_type="DEL")

  def export_one(self, export_endpoint, export_from=""):
    """Export Doc String"""
    url = endpoint_url(self.folder, "export", id="", modifier=f"{export_endpoint}", conn=self.conn)
    return request_json(url, options={"from": export_from}, payload="", conn=self.conn, request_type="GET")

  def export_all(self, export_endpoint, export_from=""):
    """Export All Doc String"""
    counter = 1
    print(f"{export_endpoint} {counter}: {export_from}")
    response = self.export_one(export_endpoint, export_from)
    data = response["data"]
    if data == []: return []
    has_more = response["hasMore"]
    while has_more:
      counter += 1
      export_from = response["continueFrom"]
      print(f"{export_endpoint} {counter}: {export_from}")
      response = self.export_one(export_endpoint, export_from)
      data.extend(response["data"])
      has_more = response["hasMore"]
    print(f"Export Data Complete. {len(data)} rows exported.")
    return data