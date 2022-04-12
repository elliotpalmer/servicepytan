# Examples

## Get Completed Jobs Between Dates

```python
import servicepytan

# Create the Jobs Endpoint Object
# API Endpoint: https://api.servicetitan.io/jpm/v2/tenant/{tenant}/jobs
# Folder: jpm, Endpoint: jobs
st_jobs_endpoint = servicepytan.Endpoint("jpm", "jobs")

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

## Get Completed Jobs using DataService

```python
import servicepytan

st_data_service = servicepytan.DataService()

data = st_data_service.get_jobs_completed_between("2022-04-06", "2022-04-07")

print(f"Number of Jobs Returned {len(data)}")
```

##