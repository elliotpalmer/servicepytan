from servicepytan.data import DataService

def get_booked_jobs_by_agent(start_date, end_date, config_file="servicepytan_config.json"):
  booked_jobs = DataService(config_file=config_file).get_jobs_created_between(start_date, end_date)
  employees = DataService(config_file=config_file).get_employees()
  pass