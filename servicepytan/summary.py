from servicepytan.data import DataService

def get_booked_jobs_by_agent(start_date, end_date, conn=None):
  booked_jobs = DataService(conn=conn).get_jobs_created_between(start_date, end_date)
  employees = DataService(conn=conn).get_employees()
  pass
