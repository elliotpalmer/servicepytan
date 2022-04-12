"""Provides methods for simplified and opininated ways of retrieving data from the ServiceTitan API"""
from servicepytan.requests import Endpoint
from servicepytan.dates import convert_date_to_api_format
from servicepytan.utils import get_timezone_by_file
class DataService:
  """Primary class for executing data methods.

  The DataService class retrieves the configuration file and authentication settings.
  The methods included are a selection of common data pulls with a simplified API generally
  based on retrieving data between a date range.

  Attributes:
      config_file: a string file path to the config file.
  """
  def __init__(self, config_file="servicepytan_config.json"):
    """Inits DataService with configuration file and authentication settings."""
    self.config_file = config_file
    self.timezone = get_timezone_by_file(config_file)

  def get_jobs_completed_between(self, start_date, end_date, job_status=["Completed","Scheduled","InProgress","Dispatched"]):
    """Retrieve all jobs completed between the start and end date"""
    data = []
    for status in job_status:
      options = {
        "jobStatus": status,
        "completedOnOrAfter": convert_date_to_api_format(start_date, self.timezone),
        "completedBefore": convert_date_to_api_format(end_date, self.timezone)
      }
      data.extend(Endpoint("jpm", "jobs").get_all(options))
    
    return data

  def get_appointments_between(self, start_date, end_date, appointment_status=["Scheduled", "Dispatched", "Working","Done"]):
    """Retrieve all appointments that start between the start and end date"""
    data = []
    for status in appointment_status:
      options = {
        "status": status,
        "startsOnOrAfter":convert_date_to_api_format(start_date, self.timezone),
        "startsBefore":convert_date_to_api_format(end_date, self.timezone)
      }
      data.extend(Endpoint("jpm", "appointments").get_all(options))
    
    return data

  def get_sold_estimates_between(self, start_date, end_date):
    """Retrieve all sold estimates that sold between the start and end date"""
    options = {
        "active": "True",
        "soldAfter":convert_date_to_api_format(start_date, self.timezone),
        "soldBefore":convert_date_to_api_format(end_date, self.timezone)
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
        "createdOnOrAfter":convert_date_to_api_format(start_date, self.timezone),
        "createdBefore":convert_date_to_api_format(end_date, self.timezone)
      }
    return Endpoint("inventory", "purchase-orders").get_all(options)
    pass

  def get_jobs_modified_between(self, start_date, end_date):
    """Retrieve all jobs modified between the start and end date"""
    options = {
      "modifiedOnOrAfter":convert_date_to_api_format(start_date, self.timezone),
      "modifiedBefore":convert_date_to_api_format(end_date, self.timezone)
    }
    data = Endpoint("jpm", "jobs").get_all(options)
    
    return data