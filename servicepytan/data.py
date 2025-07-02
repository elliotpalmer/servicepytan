"""Provides methods for simplified and opininated ways of retrieving data from the ServiceTitan API"""
from servicepytan.requests import Endpoint
from servicepytan._dates import _convert_date_to_api_format
from servicepytan.utils import get_timezone_by_file
class DataService:
  """Primary class for executing data methods.

  The DataService class retrieves the configuration file and authentication settings.
  The methods included are a selection of common data pulls with a simplified API generally
  based on retrieving data between a date range.

  Attributes:
      conn: a dictionary containing the credential config.
  """
  def __init__(self, conn=None):
    """Inits DataService with configuration file and authentication settings."""
    self.conn = conn
    self.timezone = get_timezone_by_file(conn)

  def get_jobs_completed_between(self, start_date, end_date, job_status=["Completed","Scheduled","InProgress","Dispatched"]):
    """Retrieve all jobs completed between the start and end date.
    
    Fetches jobs that were completed within the specified date range.
    Can filter by multiple job statuses simultaneously.
    
    Args:
        start_date: Start date for the query (string or datetime object)
        end_date: End date for the query (string or datetime object)
        job_status: List of job statuses to include (default includes most common statuses)
        
    Returns:
        list: Combined list of all jobs matching the criteria
        
    Examples:
        >>> data_service = DataService(conn)
        >>> jobs = data_service.get_jobs_completed_between("2024-01-01", "2024-01-31")
        >>> completed_only = data_service.get_jobs_completed_between(
        ...     "2024-01-01", "2024-01-31", job_status=["Completed"]
        ... )
    """
    data = []
    for status in job_status:
      options = {
        "jobStatus": status,
        "completedOnOrAfter": _convert_date_to_api_format(start_date, self.timezone),
        "completedBefore": _convert_date_to_api_format(end_date, self.timezone)
      }
      data.extend(Endpoint("jpm", "jobs").get_all(options))
    
    return data

  def get_jobs_created_between(self, start_date, end_date):
    """Retrieve all jobs created between the start and end date.
    
    Fetches jobs that were originally created within the specified date range,
    regardless of their current status or completion date.
    
    Args:
        start_date: Start date for the query (string or datetime object)
        end_date: End date for the query (string or datetime object)
        
    Returns:
        list: List of all jobs created in the date range
        
    Examples:
        >>> data_service = DataService(conn)
        >>> new_jobs = data_service.get_jobs_created_between("2024-01-01", "2024-01-31")
    """
    options = {
      "createdOnOrAfter": _convert_date_to_api_format(start_date, self.timezone),
      "createdBefore": _convert_date_to_api_format(end_date, self.timezone)
    }
    return Endpoint("jpm", "jobs").get_all(options)

  def get_appointments_between(self, start_date, end_date, appointment_status=["Scheduled", "Dispatched", "Working","Done"]):
    """Retrieve all appointments that start between the start and end date.
    
    Fetches appointments scheduled to start within the specified date range.
    Can filter by multiple appointment statuses simultaneously.
    
    Args:
        start_date: Start date for the query (string or datetime object)
        end_date: End date for the query (string or datetime object)
        appointment_status: List of appointment statuses to include
        
    Returns:
        list: Combined list of all appointments matching the criteria
        
    Examples:
        >>> data_service = DataService(conn)
        >>> appointments = data_service.get_appointments_between("2024-01-01", "2024-01-31")
        >>> scheduled_only = data_service.get_appointments_between(
        ...     "2024-01-01", "2024-01-31", appointment_status=["Scheduled"]
        ... )
    """
    data = []
    for status in appointment_status:
      options = {
        "status": status,
        "startsOnOrAfter":_convert_date_to_api_format(start_date, self.timezone),
        "startsBefore":_convert_date_to_api_format(end_date, self.timezone)
      }
      data.extend(Endpoint("jpm", "appointments").get_all(options))
    
    return data

  def get_sold_estimates_between(self, start_date, end_date):
    """Retrieve all sold estimates that were sold between the start and end date.
    
    Fetches estimates that were marked as sold within the specified date range.
    Only includes active (not cancelled) estimates.
    
    Args:
        start_date: Start date for the query (string or datetime object)
        end_date: End date for the query (string or datetime object)
        
    Returns:
        list: List of all sold estimates in the date range
        
    Examples:
        >>> data_service = DataService(conn)
        >>> sold_estimates = data_service.get_sold_estimates_between("2024-01-01", "2024-01-31")
    """
    options = {
        "active": "True",
        "soldAfter":_convert_date_to_api_format(start_date, self.timezone),
        "soldBefore":_convert_date_to_api_format(end_date, self.timezone)
      }
    return Endpoint("sales", "estimates").get_all(options)

  def get_total_sales_between(self, start_date, end_date):
    """Retrieves total sales dollar amount between start and end date.
    
    Calculates the total sales amount by summing all sold estimate items
    within the specified date range. This provides a quick way to get
    revenue totals for reporting.
    
    Args:
        start_date: Start date for the query (string or datetime object)
        end_date: End date for the query (string or datetime object)
        
    Returns:
        float: Total sales amount for the period
        
    Examples:
        >>> data_service = DataService(conn)
        >>> total_sales = data_service.get_total_sales_between("2024-01-01", "2024-01-31")
        >>> print(f"Total sales: ${total_sales:,.2f}")
    """
    data = self.get_sold_estimates_between(start_date, end_date)
    sales = 0
    for row in data:
      for sku in row["items"]:
        sales += sku['total']
    
    return sales

  def get_purchase_orders_created_between(self, start_date, end_date):
    """Retrieve all purchase orders created between the start and end date.
    
    Fetches purchase orders that were created within the specified date range,
    useful for tracking procurement activity and spend.
    
    Args:
        start_date: Start date for the query (string or datetime object)
        end_date: End date for the query (string or datetime object)
        
    Returns:
        list: List of all purchase orders created in the date range
        
    Examples:
        >>> data_service = DataService(conn)
        >>> pos = data_service.get_purchase_orders_created_between("2024-01-01", "2024-01-31")
    """
    options = {
        "createdOnOrAfter":_convert_date_to_api_format(start_date, self.timezone),
        "createdBefore":_convert_date_to_api_format(end_date, self.timezone)
      }
    return Endpoint("inventory", "purchase-orders").get_all(options)

  def get_jobs_modified_between(self, start_date, end_date):
    """Retrieve all jobs modified between the start and end date.
    
    Fetches jobs that were updated or modified within the specified date range,
    useful for tracking changes and updates to existing jobs.
    
    Args:
        start_date: Start date for the query (string or datetime object)
        end_date: End date for the query (string or datetime object)
        
    Returns:
        list: List of all jobs modified in the date range
        
    Examples:
        >>> data_service = DataService(conn)
        >>> modified_jobs = data_service.get_jobs_modified_between("2024-01-01", "2024-01-31")
    """
    options = {
      "modifiedOnOrAfter":_convert_date_to_api_format(start_date, self.timezone),
      "modifiedBefore":_convert_date_to_api_format(end_date, self.timezone)
    }
    data = Endpoint("jpm", "jobs").get_all(options)
    
    return data

  def get_employees(self, active="True"):
    """Retrieve employee list.
    
    Fetches the list of employees from ServiceTitan. Can filter to show
    only active employees or include inactive ones as well.
    
    Args:
        active: String indicating whether to show only active employees ("True" or "False")
        
    Returns:
        list: List of employee records
        
    Examples:
        >>> data_service = DataService(conn)
        >>> active_employees = data_service.get_employees()
        >>> all_employees = data_service.get_employees(active="False")
    """
    options = {
        "active": active
      }
    return Endpoint("settings", "employees").get_all(options)

  def get_technicians(self, active="True"):
    """Retrieve technician list.
    
    Fetches the list of technicians from ServiceTitan. Technicians are
    a subset of employees who perform field work.
    
    Args:
        active: String indicating whether to show only active technicians ("True" or "False")
        
    Returns:
        list: List of technician records
        
    Examples:
        >>> data_service = DataService(conn)
        >>> active_techs = data_service.get_technicians()
        >>> all_techs = data_service.get_technicians(active="False")
    """
    options = {
        "active": active
      }
    return Endpoint("settings", "technicians").get_all(options)

  def get_tag_types(self, active="True"):
    """Retrieve tag types list.
    
    Fetches the list of tag types configured in ServiceTitan. Tag types
    are used to categorize and organize jobs, customers, and other entities.
    
    Args:
        active: String indicating whether to show only active tag types ("True" or "False")
        
    Returns:
        list: List of tag type records
        
    Examples:
        >>> data_service = DataService(conn)
        >>> tag_types = data_service.get_tag_types()
    """
    options = {
        "active": active
      }
    return Endpoint("settings", "tag-types").get_all(options)

  def get_business_units(self, active="True"):
    """Retrieve business units list.
    
    Fetches the list of business units configured in ServiceTitan. Business
    units are used to organize operations by service type, location, or other criteria.
    
    Args:
        active: String indicating whether to show only active business units ("True" or "False")
        
    Returns:
        list: List of business unit records
        
    Examples:
        >>> data_service = DataService(conn)
        >>> business_units = data_service.get_business_units()
    """
    options = {
        "active": active
      }
    return Endpoint("settings", "business-units").get_all(options)