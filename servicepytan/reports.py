import math
from servicepytan.utils import request_json, get_timezone_by_file, endpoint_url, request_json_with_retry

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

def get_report_categories(conn=None):
    """Get a list of report categories from ServiceTitan.
    
    Retrieves all available report categories from the ServiceTitan reporting API.
    These categories are used to organize reports and are required for accessing
    specific reports.
    
    Args:
        conn: Dictionary containing the credential configuration
        
    Returns:
        dict: JSON response containing list of report categories
        
    Raises:
        requests.HTTPError: If the API request fails
        
    Examples:
        >>> categories = get_report_categories(conn)
        >>> for category in categories['data']:
        ...     print(category['name'])
    """
    return request_json(endpoint_url('reporting', 'report-categories', conn=conn), conn=conn)

def get_report_list(report_category, conn=None):
    """Get a list of reports for a given report category.
    
    Retrieves all available reports within a specific category from the
    ServiceTitan reporting API.
    
    Args:
        report_category: The category ID or name to retrieve reports for
        conn: Dictionary containing the credential configuration
        
    Returns:
        dict: JSON response containing list of reports in the category
        
    Raises:
        requests.HTTPError: If the API request fails
        
    Examples:
        >>> reports = get_report_list("jobs", conn)
        >>> for report in reports['data']:
        ...     print(f"{report['id']}: {report['name']}")
    """
    return request_json(endpoint_url('reporting', f'report-category/{report_category}/reports', conn=conn), conn=conn)

def get_dynamic_set_list(dynamic_set_id,conn=None):
    """Get a list of dynamic value sets for report parameters.
    
    Retrieves the available values for dynamic parameters in ServiceTitan reports.
    Dynamic sets contain the possible values that can be selected for certain
    report parameters.
    
    Args:
        dynamic_set_id: The ID of the dynamic value set to retrieve
        conn: Dictionary containing the credential configuration
        
    Returns:
        dict: JSON response containing the dynamic value set data
        
    Raises:
        requests.HTTPError: If the API request fails
        
    Examples:
        >>> dynamic_values = get_dynamic_set_list("employees", conn)
        >>> for value in dynamic_values['data']:
        ...     print(f"{value['id']}: {value['name']}")
    """
    return request_json(endpoint_url('reporting', f'dynamic-value-sets/{dynamic_set_id}', conn=conn), conn=conn)

class Report:
  """Primary class for retrieving Reporting Endpoint Data.

  Provides a comprehensive interface for working with ServiceTitan reports,
  including parameter management, metadata retrieval, and data extraction.

  Attributes:
      category: A string representing the report category. Find list of categories with get_report_categories().
      report_id: A string representing the report id. Find list of report_id using get_report_list().
      conn: a dictionary containing the credential config.
  """
  def __init__(self, category, report_id, conn=None):
    """Initialize Report with category, report ID, and connection configuration.
    
    Args:
        category: The report category (e.g., "jobs", "customers")
        report_id: The specific report ID within the category
        conn: Dictionary containing the credential configuration
    """
    self.conn = conn
    # self.timezone = get_timezone_by_file(conn)
    self.category = category
    self.report_id = report_id
    self.params = {"parameters": []}
    self.metadata = self.get_metadata()

  def add_params(self, name, value):
    """Add or update a parameter for the report.
    
    Adds a new parameter to the report's parameter list. If the parameter
    already exists, it updates the existing value.
    
    Args:
        name: The parameter name as defined in the report metadata
        value: The value to set for the parameter
        
    Examples:
        >>> report = Report("jobs", "job-summary", conn)
        >>> report.add_params("StartDate", "2024-01-01")
        >>> report.add_params("BusinessUnit", "12345")
    """
    param_keys = [param["name"] for param in self.params["parameters"]]
    if name in param_keys:
      logger.info(f"Parameter '{name}' already exists. Updating value from '{self.params['parameters'][param_keys.index(name)]['value']}' to '{value}'...")
      self.update_params(name, value)
    else:
      self.params["parameters"].append({"name": name, "value": value})

  def update_params(self, name, value):
    """Update an existing parameter in the report.
    
    Updates the value of an existing parameter. If the parameter doesn't exist,
    it will be added to the parameter list.
    
    Args:
        name: The parameter name to update
        value: The new value for the parameter
        
    Examples:
        >>> report.update_params("StartDate", "2024-02-01")
    """
    param_keys = [param["name"] for param in self.params["parameters"]]
    if name in param_keys:
      self.params["parameters"][param_keys.index(name)]["value"] = value
    else:
      logger.info(f"Parameter '{name}' does not exist. Adding parameter...")
      self.add_params(name, value)

  def get_params(self):
    """Get the current report parameters.
    
    Returns the current parameter configuration for the report.
    
    Returns:
        dict: Dictionary containing the report parameters
        
    Examples:
        >>> current_params = report.get_params()
        >>> print(current_params)
    """
    return self.params

  def get_metadata(self):
    """Get report metadata including available parameters and their types.
    
    Retrieves comprehensive metadata about the report, including parameter
    definitions, data types, required fields, and available values.
    
    Returns:
        dict: JSON response containing report metadata
        
    Raises:
        requests.HTTPError: If the API request fails
        
    Examples:
        >>> metadata = report.get_metadata()
        >>> for param in metadata['parameters']:
        ...     print(f"{param['name']}: {param['dataType']}")
    """
    endpoint = f"report-category/{self.category}/reports/{self.report_id}"
    url = endpoint_url("reporting",endpoint, conn=self.conn)
    return request_json_with_retry(url, conn=self.conn)

  def show_param_types(self):
    """Display parameter types and requirements in a formatted way.
    
    Prints a formatted list of all report parameters showing their names,
    data types, whether they're required, and any available values.
    
    Examples:
        >>> report.show_param_types()
        >>> # Output:
        >>> # [*] - StartDate: DateTime
        >>> # [ ] - BusinessUnit: Long (dynamicSetId: 123)
        >>> #   - Business Unit 1
        >>> #   - Business Unit 2
    """
    for param in self.metadata["parameters"]:
      dynamic_set_id = ""
      required = "[ ]"
      accepted_values = []
      if param["isRequired"]:
        required = "[*]"
      if param['acceptValues']:
        dynamic_set_id = f" (dynamicSetId: {param['acceptValues']['dynamicSetId']})"
        if param['acceptValues']['values']:
          accepted_values = param['acceptValues']['values']
      logger.info(f"{required} - {param['name']}: {param['dataType']}, {dynamic_set_id}")
      for value in accepted_values:
        logger.info(f"  - {value}")

  def get_data(self, params="", page=1, page_size=5000):
    """Get report data for a specific page.
    
    Retrieves report data from ServiceTitan for a single page. Used internally
    by get_all_data() for pagination, but can be used directly for custom
    pagination handling.
    
    Args:
        params: Parameter configuration (uses instance params if empty)
        page: Page number to retrieve (1-based)
        page_size: Number of records per page (max 5000)
        
    Returns:
        dict: JSON response containing report data and pagination info
        
    Raises:
        requests.HTTPError: If the API request fails
        
    Examples:
        >>> report.add_params("StartDate", "2024-01-01")
        >>> page_data = report.get_data(page=1, page_size=1000)
        >>> print(f"Retrieved {len(page_data['data'])} records")
    """
    if params == "":
      params = self.params
    options = {"page": page, "pageSize": page_size, "includeTotal": True}
    endpoint = f"report-category/{self.category}/reports/{self.report_id}/data"
    url = endpoint_url("reporting",endpoint, conn=self.conn)
    return request_json_with_retry(url, options=options, json_payload=params, 
              conn=self.conn, request_type="POST")
  
  def get_all_data(self, params="", page_size=5000, timeout_min=60):
    """Get all report data with automatic pagination.
    
    Retrieves all available data from the report by automatically handling
    pagination. Includes intelligent page size optimization and timeout
    protection to prevent excessively long-running requests.
    
    Args:
        params: Parameter configuration (uses instance params if empty)
        page_size: Number of records per page (max 5000)
        timeout_min: Maximum time in minutes before aborting the request
        
    Returns:
        dict: Dictionary containing 'data' (list of records) and 'fields' (metadata)
        
    Raises:
        requests.HTTPError: If any API request fails
        
    Examples:
        >>> report = Report("jobs", "job-summary", conn)
        >>> report.add_params("StartDate", "2024-01-01")
        >>> report.add_params("EndDate", "2024-01-31")
        >>> all_data = report.get_all_data()
        >>> print(f"Retrieved {len(all_data['data'])} total records")
        
        >>> # For large datasets, use smaller timeout
        >>> large_report_data = report.get_all_data(timeout_min=30)
    """
    page = 1
    data = []
    fields = []
    if params == "":
      params = self.params
    logger.info("Getting first page of data...")
    response = self.get_data(params, page=page, page_size=page_size)
    data.extend(response["data"])
    fields.extend(response["fields"])
    total = response["totalCount"]
    has_more = response["hasMore"]
    logger.info(f"Retrieved {len(data)} of {total} records...")
    requests_needed = math.ceil(total / page_size)
    mins_to_complete = requests_needed * 5
    updated_page_size = page_size
    if mins_to_complete > timeout_min:
      init_page_size = updated_page_size
      if page_size < 5000 and math.ceil(total / 5000) < 12:
        logger.info("Setting page size to 5000 to speed up report retrieval...")
        updated_page_size = 5000
        requests_needed = 1 + math.ceil((total - init_page_size) / updated_page_size)
      else:
        logger.warning(f"This request will take at least {mins_to_complete/60} hours to complete.")
        logger.warning("Limit the parameters to reduce the number of requests and try again.")
        return {"error": "Too many requests. Try again with fewer parameters."}
    while has_more:
      page += 1
      logger.info(f"Getting page {page} of {requests_needed}...")
      response = self.get_data(params, page=page, page_size=updated_page_size)
      if(len(response["data"]) == 0):
        logger.info("No more data to retrieve.")
        break
      data.extend(response["data"])
      logger.info(f"Retrieved {len(data)} sof {total} records...")
      has_more = response["hasMore"]
    return {"data": data, "fields": fields}