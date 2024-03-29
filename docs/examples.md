# Examples

## Completed Jobs

### Get Completed Jobs Between Dates

```python
import servicepytan

# Create the Jobs Endpoint Object
# API Endpoint: https://api.servicetitan.io/jpm/v2/tenant/{tenant}/jobs
# Folder: jpm, Endpoint: jobs
st_conn = servicepytan.auth.servicepytan_connect(config_file="./servicepytan_config.json")
st_jobs_endpoint = servicepytan.Endpoint("jpm", "jobs", conn=st_conn)

options = {
  "pageSize":"50", # Number of jobs to return per API Request
  "page":"1", # Which page to return 
  "active":"true", # Only jobs that are active
  "jobStatus" : "Completed", 
  "completedOnOrAfter":"2022-04-06T00:04:00Z", # Date in UTC Timezone
  "completedBefore":"2022-04-07T00:04:00Z" # Date in UTC Timezone
}

# The .get_all() method makes requests until all records are returned
job_json = st_jobs_endpoint.get_all(options)

# The object returned has a 'data' element that is a list of job objects
jobs_data = job_json['data']

# Print the number of records to simplify the output
print(f"Number of Jobs Returned: {len(jobs_data)}")
```

### Get Completed Jobs using DataService

```python
import servicepytan
st_conn = servicepytan.auth.servicepytan_connect(config_file="./servicepytan_config.json")
st_data_service = servicepytan.DataService(conn=st_conn)

data = st_data_service.get_jobs_completed_between("2022-04-06", "2022-04-07")

print(f"Number of Jobs Returned {len(data)}")
```

## Custom Reports
```python
# Import the functions and reporting class
from servicepytan import Report, auth
from servicepytan.reports import get_report_categories, get_report_list

# Set your config file path
st_conn = servicepytan.auth.servicepytan_connect(config_file="./servicepytan_config.json")

# Retrieve a list of report categories
categories = get_report_categories(config_file_path, conn=st_conn)
print(categories)

# Retrieve a list of reports included in the category 
category_report_list = get_report_list("operations", config_file_path, conn=st_conn)
print(category_report_list)

# Configure a specific report
# NOTE: this is a standard ServiceTitan report in the Operations category
custom_report = Report("operations", "94428310", conn=st_conn)

# Look at the reporting metadata
# This inclued the filter options and field information
print(custom_report.metadata)

# Get list of parameters
custom_report.show_param_types()
# NOTE: [*] indicates a required parameter
# [*] - DateType: Number,  (dynamicSetId: job-date-filter-type)
# [*] - From: Date, 
# [*] - To: Date, 
# [ ] - BusinessUnitId: Number,  (dynamicSetId: business-units)
# [ ] - IncludeAdjustmentInvoices: Boolean, 

# Get dynamic set information if needed
dynamic_sets = get_dynamic_set_list(dynamic_set_id='job-date-filter-type',conn=st_conn)
print(dynamic_sets)
# [0, 'Invoice Date'],
# [1, 'Job Completion Date'],
# [2, 'Job Creation Date'],
# [3, 'Job Start Date'],
# [4, 'Last Paid On Date'],
# [5, 'First Dispatch'],
# [6, 'Jobs with Appt Date'],
# [7, 'Jobs with Next Appt Start Date']

# Add Report Parameters
custom_report.add_params("DateType","3")
custom_report.add_params("From", "2022-11-03")
custom_report.add_params("To", "2022-11-03")
print(custom_report.get_params())

# Get individual page of data
custom_report_page_1_data = custom_report.get_data() #defaults to page 1
print(custom_report_page_1_data)

# Get all data
# This will run requests until all pages have been retrieved.
# NOTE: There is a 5min wait between subsequent requests from the same report.
#       The function will automatically wait during the delay, however if it expects to 
#       run for more than 1 hour. The function will exit and ask to reduce size of request.
custom_report_all_data = custom_report.get_all_data()
```
