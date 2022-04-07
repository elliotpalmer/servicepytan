from servicepytan.requests import Endpoint

class DataService:
  def __init__(self, key_file="st_api_credentials.json"):
    self.key_file = key_file

  def get_jobs_between(self, start_date, end_date, job_status=["Completed","Scheduled","InProgress","Dispatched"]):
    data = []
    for status in job_status:
      options = {
        "jobStatus": status,
        "completedOnOrAfter":start_date,
        "completedBefore":end_date
      }
      data.extend(Endpoint("jpm", "jobs").get_all(options))
    
    return data

  def get_appointments_between(self, start_date, end_date, appointment_status=["Scheduled", "Dispatched", "Working","Done"]):
    data = []
    for status in appointment_status:
      options = {
        "status": status,
        "startsOnOrAfter":start_date,
        "startsBefore":end_date
      }
      data.extend(Endpoint("jpm", "appointments").get_all(options))
    
    return data

  def get_sold_estimates_between(self, start_date, end_date):
    options = {
        "active": "True",
        "soldAfter":start_date,
        "soldBefore":end_date
    }
    return Endpoint("sales", "estimates").get_all(options)

  def get_total_sales_between(self, start_date, end_date):
    data = self.get_sold_estimates_between(start_date, end_date)
    sales = 0
    for row in data:
      for sku in row["items"]:
        sales += sku['total']
    
    return sales