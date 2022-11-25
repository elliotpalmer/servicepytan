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
    """Retrieve all jobs completed between the start and end date"""
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
    """Retrieve all jobs created between the start and end date"""
    options = {
      "createdOnOrAfter": _convert_date_to_api_format(start_date, self.timezone),
      "createdBefore": _convert_date_to_api_format(end_date, self.timezone)
    }
    return Endpoint("jpm", "jobs").get_all(options)

  def get_appointments_between(self, start_date, end_date, appointment_status=["Scheduled", "Dispatched", "Working","Done"]):
    """Retrieve all appointments that start between the start and end date"""
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
    """Retrieve all sold estimates that sold between the start and end date"""
    options = {
        "active": "True",
        "soldAfter":_convert_date_to_api_format(start_date, self.timezone),
        "soldBefore":_convert_date_to_api_format(end_date, self.timezone)
      }
    return Endpoint("sales", "estimates").get_all(options)

  def get_total_sales_between(self, start_date, end_date):
    """Retrieves total sales $ between start and end date"""
    data = self.get_sold_estimates_between(start_date, end_date)
    sales = 0
    for row in data:
      for sku in row["items"]:
        sales += sku['total']
    
    return sales

  def get_purchase_orders_created_between(self, start_date, end_date):
    """Retrieve all purchase orders between the start and end date"""
    options = {
        "createdOnOrAfter":_convert_date_to_api_format(start_date, self.timezone),
        "createdBefore":_convert_date_to_api_format(end_date, self.timezone)
      }
    return Endpoint("inventory", "purchase-orders").get_all(options)

  def get_jobs_modified_between(self, start_date, end_date):
    """Retrieve all jobs modified between the start and end date"""
    options = {
      "modifiedOnOrAfter":_convert_date_to_api_format(start_date, self.timezone),
      "modifiedBefore":_convert_date_to_api_format(end_date, self.timezone)
    }
    data = Endpoint("jpm", "jobs").get_all(options)
    
    return data

  def get_employees(self, active="True"):
    """Retrieve active employee list"""
    options = {
        "active": active
      }
    return Endpoint("settings", "employees").get_all(options)

  def get_technicians(self, active="True"):
    """Retrieve active technician list"""
    options = {
        "active": active
      }
    return Endpoint("settings", "technicians").get_all(options)

  def get_tag_types(self, active="True"):
    """Retrieve active tag-types list"""
    options = {
        "active": active
      }
    return Endpoint("settings", "tag-types").get_all(options)

  def get_business_units(self, active="True"):
    """Retrieve active business units list"""
    options = {
        "active": active
      }
    return Endpoint("settings", "business-units").get_all(options)