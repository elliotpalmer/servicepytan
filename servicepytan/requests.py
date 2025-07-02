from servicepytan.utils import request_json_with_retry, check_default_options, endpoint_url

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

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
  def get_one(self, id, modifier="", query={}):
    """Retrieve one record using the record id.
    
    Fetches a single record from the API endpoint using its unique identifier.
    Optionally supports modifiers to access sub-resources and query parameters
    for additional filtering.
    
    Args:
        id: The unique identifier of the record to retrieve
        modifier: Optional sub-resource path (e.g., "notes" to get job notes)
        query: Optional dictionary of query parameters for filtering
        
    Returns:
        dict: JSON response containing the requested record data
        
    Raises:
        requests.HTTPError: If the API request fails
        
    Examples:
        >>> endpoint = Endpoint("jpm", "jobs", conn)
        >>> job = endpoint.get_one(id="12345678")
        >>> job_notes = endpoint.get_one(id="12345678", modifier="notes")
    """
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=modifier, conn=self.conn)
    options = check_default_options(query)
    return request_json_with_retry(url, options=options, payload="", conn=self.conn, request_type="GET")

  def get_many(self, query={}, id="", modifier=""):
    """Retrieve one page of results with query options to customize.

    Fetches a single page of results from the API endpoint. Even though this is a 
    "get_many" request, it can still use an id and modifier for accessing 
    sub-resources (e.g., getting Notes for a specific Job).
    
    Args:
        query: Dictionary of query parameters for filtering and pagination
        id: Optional record ID for accessing sub-resources
        modifier: Optional sub-resource path
        
    Returns:
        dict: JSON response containing paginated results with 'data' and 'hasMore' fields
        
    Raises:
        requests.HTTPError: If the API request fails
        
    Examples:
        >>> endpoint = Endpoint("jpm", "jobs", conn)
        >>> page_data = endpoint.get_many(query={"pageSize": 50, "page": 1})
        >>> job_notes = endpoint.get_many(id="12345678", modifier="notes")
    """
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=modifier, conn=self.conn)
    options = check_default_options(query)
    return request_json_with_retry(url, options, payload="", conn=self.conn, request_type="GET")
  
  def get_all(self, query={}, id="", modifier=""):
    """Retrieve all pages of results for your query.
    
    Automatically handles pagination by making multiple API calls to fetch all
    available records that match the query criteria. This method continues
    fetching pages until no more data is available.
    
    Args:
        query: Dictionary of query parameters for filtering (page parameter will be managed automatically)
        id: Optional record ID for accessing sub-resources
        modifier: Optional sub-resource path
        
    Returns:
        list: Combined list of all records from all pages
        
    Raises:
        requests.HTTPError: If any API request fails
        
    Examples:
        >>> endpoint = Endpoint("jpm", "jobs", conn)
        >>> all_jobs = endpoint.get_all(query={"jobStatus": "Completed"})
        >>> all_job_notes = endpoint.get_all(id="12345678", modifier="notes")
    """
    query["page"] = "1"
    logger.info(query)
    response = self.get_many(query=query, id=id, modifier=modifier)
    data = response["data"]
    if data == []: return []
    has_more = response["hasMore"]
    while has_more:
      query["page"] = str(int(query["page"]) + 1)
      logger.info(query)
      response = self.get_many(query=query, id=id, modifier=modifier)
      data.extend(response["data"])
      has_more = response["hasMore"]

    return data

  def create(self, payload):
    """Create a new record via POST request.
    
    Sends a POST request to create a new resource in the API endpoint.
    The payload should contain all required fields for the resource type.
    
    Args:
        payload: Dictionary containing the data for the new record
        
    Returns:
        dict: JSON response from the API, typically containing the created record
        
    Raises:
        requests.HTTPError: If the API request fails
        
    Examples:
        >>> endpoint = Endpoint("jpm", "jobs", conn)
        >>> new_job = {
        ...     "summary": "New Job",
        ...     "customerId": 12345,
        ...     "businessUnitId": 67890
        ... }
        >>> created_job = endpoint.create(new_job)
    """
    url = endpoint_url(self.folder, self.endpoint, conn=self.conn)
    return request_json_with_retry(url, options={}, json_payload=payload, conn=self.conn, request_type="POST")

  def update(self, id, payload, modifier="", request_type="PUT"):
    """Update an existing record via PUT or PATCH request.
    
    Sends a PUT or PATCH request to update an existing resource. PUT is used
    for complete updates while PATCH can be used for partial updates.
    
    Args:
        id: The unique identifier of the record to update
        payload: Dictionary containing the updated data
        modifier: Optional sub-resource path for updating specific parts
        request_type: HTTP method type ("PUT" or "PATCH"), defaults to "PUT"
        
    Returns:
        dict: JSON response from the API
        
    Raises:
        requests.HTTPError: If the API request fails
        
    Examples:
        >>> endpoint = Endpoint("jpm", "jobs", conn)
        >>> updates = {"summary": "Updated Job Summary"}
        >>> updated_job = endpoint.update("12345678", updates)
        >>> updated_job = endpoint.update("12345678", updates, request_type="PATCH")
    """
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=modifier, conn=self.conn)
    return request_json_with_retry(url, options={}, payload=payload, conn=self.conn, request_type=request_type)

  def delete(self, id, modifier=""):
    """Delete a record via DELETE request.
    
    Sends a DELETE request to remove a resource from the API endpoint.
    
    Args:
        id: The unique identifier of the record to delete
        modifier: Optional sub-resource path for deleting specific parts
        
    Returns:
        dict: JSON response from the API
        
    Raises:
        requests.HTTPError: If the API request fails
        
    Examples:
        >>> endpoint = Endpoint("jpm", "jobs", conn)
        >>> result = endpoint.delete("12345678")
    """
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=f"{modifier}", conn=self.conn)
    return request_json_with_retry(url, options={}, payload="", conn=self.conn, request_type="DEL")

  def delete_subitem(self, id, modifier_id, modifier):
    """Delete a sub-item of a record via DELETE request.
    
    Sends a DELETE request to remove a specific sub-resource that belongs to
    a parent resource. This is useful for deleting nested items like notes,
    attachments, or other related records.
    
    Args:
        id: The unique identifier of the parent record
        modifier_id: The unique identifier of the sub-item to delete
        modifier: The sub-resource type (e.g., "notes", "attachments")
        
    Returns:
        dict: JSON response from the API
        
    Raises:
        requests.HTTPError: If the API request fails
        
    Examples:
        >>> endpoint = Endpoint("jpm", "jobs", conn)
        >>> result = endpoint.delete_subitem("12345678", "note_id", "notes")
    """
    url = endpoint_url(self.folder, self.endpoint, id=id, modifier=f"{modifier}/{modifier_id}", conn=self.conn)
    return request_json_with_retry(url, options={}, payload="", conn=self.conn, request_type="DEL")

  def export_one(self, export_endpoint, export_from="", include_recent_changes=False):
    """Export one page of data from an export endpoint.
    
    Retrieves one page of export data from ServiceTitan's export endpoints,
    which are optimized for bulk data extraction and typically return larger
    datasets than regular API endpoints.
    
    Args:
        export_endpoint: The specific export endpoint to call
        export_from: Continuation token from previous export call for pagination
        include_recent_changes: Whether to include recent changes in the export
        
    Returns:
        dict: JSON response containing export data and pagination information
        
    Raises:
        requests.HTTPError: If the API request fails
        
    Examples:
        >>> endpoint = Endpoint("jpm", "export", conn)
        >>> export_data = endpoint.export_one("jobs")
        >>> next_page = endpoint.export_one("jobs", export_from=export_data["continueFrom"])
    """
    url = endpoint_url(self.folder, "export", id="", modifier=f"{export_endpoint}", conn=self.conn)
    return request_json_with_retry(url, options={"from": export_from, "includeRecentChanges": include_recent_changes}, payload="", conn=self.conn, request_type="GET")

  def export_all(self, export_endpoint, export_from="", include_recent_changes=False):
    """Export all data from an export endpoint.
    
    Retrieves all available data from ServiceTitan's export endpoints by
    automatically handling pagination. This method continues making requests
    until all data has been retrieved.
    
    Args:
        export_endpoint: The specific export endpoint to call
        export_from: Starting continuation token (empty string to start from beginning)
        include_recent_changes: Whether to include recent changes in the export
        
    Returns:
        list: Combined list of all exported records
        
    Raises:
        requests.HTTPError: If any API request fails
        
    Examples:
        >>> endpoint = Endpoint("jpm", "export", conn)
        >>> all_jobs = endpoint.export_all("jobs")
        >>> recent_jobs = endpoint.export_all("jobs", include_recent_changes=True)
    """
    counter = 1
    logger.info(f"{export_endpoint} {counter}: {export_from}")
    response = self.export_one(export_endpoint, export_from, include_recent_changes)
    data = response["data"]
    if data == []: return []
    has_more = response["hasMore"]
    while has_more:
      counter += 1
      export_from = response["continueFrom"]
      logger.info(f"{export_endpoint} {counter}: {export_from}")
      response = self.export_one(export_endpoint, export_from, include_recent_changes)
      data.extend(response["data"])
      has_more = response["hasMore"]
    logger.info(f"Export Data Complete. {len(data)} rows exported.")
    return data