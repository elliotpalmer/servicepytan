# Examples

This guide provides comprehensive examples for using ServicePytan to interact with the ServiceTitan API. Examples progress from basic usage to advanced patterns.

## Quick Start Examples

### Basic Job Retrieval

```python
import servicepytan

# Create connection (using config file)
conn = servicepytan.auth.servicepytan_connect(config_file="./config.json")

# Get a specific job by ID
jobs_endpoint = servicepytan.Endpoint("jpm", "jobs", conn=conn)
job = jobs_endpoint.get_one(138517400)

print(f"Job #{job['jobNumber']} - Status: {job['jobStatus']}")
```

### Environment Configuration

```python
import servicepytan

# Production environment (default)
prod_conn = servicepytan.auth.servicepytan_connect(
    api_environment="production",
    config_file="./prod_config.json"
)

# Integration environment for testing
test_conn = servicepytan.auth.servicepytan_connect(
    api_environment="integration", 
    config_file="./test_config.json"
)

# Use different connections for different purposes
prod_jobs = servicepytan.Endpoint("jpm", "jobs", conn=prod_conn)
test_jobs = servicepytan.Endpoint("jpm", "jobs", conn=test_conn)
```

## Endpoint Class Examples

### Retrieving Jobs with Filters

```python
import servicepytan

conn = servicepytan.auth.servicepytan_connect(config_file="./config.json")
jobs_endpoint = servicepytan.Endpoint("jpm", "jobs", conn=conn)

# Get completed jobs within date range
options = {
    "pageSize": 50,
    "jobStatus": "Completed",
    "completedOnOrAfter": "2024-01-01T00:00:00Z",
    "completedBefore": "2024-01-31T23:59:59Z"
}

# get_all() automatically handles pagination
all_jobs = jobs_endpoint.get_all(options)
print(f"Retrieved {len(all_jobs)} completed jobs")

# Get just one page of results
first_page = jobs_endpoint.get_page(options, page=1)
print(f"First page contains {len(first_page['data'])} jobs")
```

### Working with Customers

```python
import servicepytan

conn = servicepytan.auth.servicepytan_connect()
customers_endpoint = servicepytan.Endpoint("crm", "customers", conn=conn)

# Get all active customers
active_customers = customers_endpoint.get_all({"active": "true"})

# Get a specific customer with their contacts
customer_id = 12345678
customer = customers_endpoint.get_one(customer_id)
customer_contacts = customers_endpoint.get_one(customer_id, modifier="contacts")

print(f"Customer: {customer['name']}")
print(f"Number of contacts: {len(customer_contacts)}")
```

### Creating and Updating Records

```python
import servicepytan

conn = servicepytan.auth.servicepytan_connect()
customers_endpoint = servicepytan.Endpoint("crm", "customers", conn=conn)

# Create a new customer
new_customer_data = {
    "name": "Acme Corporation",
    "type": "Commercial",
    "address": {
        "street": "123 Main St",
        "city": "Anytown", 
        "state": "NY",
        "zip": "12345"
    }
}

created_customer = customers_endpoint.post(new_customer_data)
customer_id = created_customer['id']

# Update customer information
update_data = {
    "phone": "(555) 123-4567",
    "email": "contact@acme.com"
}

updated_customer = customers_endpoint.patch(customer_id, update_data)
print(f"Updated customer: {updated_customer['name']}")
```

## DataService Examples

The DataService class provides simplified methods for common data operations.

### Jobs Data

```python
import servicepytan

conn = servicepytan.auth.servicepytan_connect()
data_service = servicepytan.DataService(conn=conn)

# Get jobs completed in date range (simplified interface)
jobs = data_service.get_jobs_completed_between("2024-01-01", "2024-01-31")
print(f"Found {len(jobs)} completed jobs")

# Filter by specific job statuses
active_jobs = data_service.get_jobs_completed_between(
    "2024-01-01", 
    "2024-01-31",
    job_status=["Scheduled", "InProgress", "Dispatched"]
)

# Get jobs created in date range
new_jobs = data_service.get_jobs_created_between("2024-01-01", "2024-01-31")
```

### Customer Data

```python
import servicepytan

data_service = servicepytan.DataService(conn=conn)

# Get customers created in date range
new_customers = data_service.get_customers_created_between("2024-01-01", "2024-01-31")

# Get customers updated in date range  
updated_customers = data_service.get_customers_updated_between("2024-01-01", "2024-01-31")

print(f"New customers: {len(new_customers)}")
print(f"Updated customers: {len(updated_customers)}")
```

### Invoice Data

```python
import servicepytan

data_service = servicepytan.DataService(conn=conn)

# Get invoices completed in date range
invoices = data_service.get_invoices_completed_between("2024-01-01", "2024-01-31")

# Get invoices exported in date range
exported_invoices = data_service.get_invoices_exported_between("2024-01-01", "2024-01-31")

# Calculate total invoice amount
total_amount = sum(invoice.get('total', 0) for invoice in invoices)
print(f"Total invoice amount: ${total_amount:,.2f}")
```

## Custom Reports Examples

ServicePytan provides comprehensive support for ServiceTitan's custom reporting system.

### Basic Report Usage

```python
import servicepytan
from servicepytan.reports import get_report_categories, get_report_list

conn = servicepytan.auth.servicepytan_connect()

# Discover available reports
categories = get_report_categories(conn=conn)
print("Available report categories:")
for category in categories['data']:
    print(f"- {category['name']}")

# Get reports in a specific category
operations_reports = get_report_list("operations", conn=conn)
print("Operations reports:")
for report in operations_reports['data']:
    print(f"- {report['name']} (ID: {report['id']})")
```

### Working with Report Parameters

```python
import servicepytan
from servicepytan.reports import get_dynamic_set_list

# Create report instance
report = servicepytan.Report("operations", "94428310", conn=conn)

# Examine report metadata
print("Report metadata:")
print(f"Name: {report.metadata['name']}")
print(f"Description: {report.metadata['description']}")

# Show required and optional parameters
report.show_param_types()
# Output shows:
# [*] - DateType: Number,  (dynamicSetId: job-date-filter-type)
# [*] - From: Date, 
# [*] - To: Date, 
# [ ] - BusinessUnitId: Number,  (dynamicSetId: business-units)

# Get dynamic set options
date_filter_options = get_dynamic_set_list(
    dynamic_set_id='job-date-filter-type', 
    conn=conn
)
print("Date filter options:")
for option in date_filter_options:
    print(f"- {option[1]} (Value: {option[0]})")
```

### Retrieving Report Data

```python
import servicepytan

report = servicepytan.Report("operations", "94428310", conn=conn)

# Set required parameters
report.add_params("DateType", "1")  # Job Completion Date
report.add_params("From", "2024-01-01")
report.add_params("To", "2024-01-31")

# Optional parameters
report.add_params("BusinessUnitId", "12345")  # Specific business unit

# Get single page of data
page_data = report.get_data(page=1)
print(f"Page 1 contains {len(page_data['data'])} records")

# Get all data (handles pagination automatically)
# Note: Large reports may take time due to 5-minute delay between requests
all_data = report.get_all_data()
print(f"Total records: {len(all_data)}")

# Process report data
for record in all_data[:5]:  # Show first 5 records
    print(record)
```

## Advanced Usage Patterns

### Error Handling and Retries

```python
import servicepytan
import logging

# Enable logging to see retry attempts
logging.basicConfig(level=logging.INFO)

conn = servicepytan.auth.servicepytan_connect()

try:
    endpoint = servicepytan.Endpoint("jpm", "jobs", conn=conn)
    
    # API calls automatically retry on transient failures
    jobs = endpoint.get_all({"pageSize": 100})
    
except servicepytan.requests.HTTPError as e:
    print(f"API request failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Batch Operations

```python
import servicepytan
from concurrent.futures import ThreadPoolExecutor

conn = servicepytan.auth.servicepytan_connect()

def get_job_details(job_id):
    """Get detailed job information including notes and appointments"""
    endpoint = servicepytan.Endpoint("jpm", "jobs", conn=conn)
    
    job = endpoint.get_one(job_id)
    notes = endpoint.get_one(job_id, modifier="notes")
    appointments = endpoint.get_one(job_id, modifier="appointments")
    
    return {
        'job': job,
        'notes': notes,
        'appointments': appointments
    }

# Get details for multiple jobs concurrently
job_ids = [12345, 12346, 12347, 12348, 12349]

with ThreadPoolExecutor(max_workers=5) as executor:
    job_details = list(executor.map(get_job_details, job_ids))

print(f"Retrieved details for {len(job_details)} jobs")
```

### Working with Large Datasets

```python
import servicepytan
import pandas as pd

conn = servicepytan.auth.servicepytan_connect()
data_service = servicepytan.DataService(conn=conn)

# Process large date range in chunks
start_date = "2024-01-01"
end_date = "2024-12-31"

# Get jobs in monthly chunks to avoid memory issues
import datetime
from dateutil.relativedelta import relativedelta

all_jobs = []
current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
end_date_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")

while current_date < end_date_dt:
    chunk_end = min(current_date + relativedelta(months=1), end_date_dt)
    
    chunk_jobs = data_service.get_jobs_completed_between(
        current_date.strftime("%Y-%m-%d"),
        chunk_end.strftime("%Y-%m-%d")
    )
    
    all_jobs.extend(chunk_jobs)
    print(f"Processed {current_date.strftime('%Y-%m')}: {len(chunk_jobs)} jobs")
    
    current_date = chunk_end

# Convert to pandas DataFrame for analysis
df = pd.DataFrame(all_jobs)
print(f"Total jobs: {len(df)}")
print(f"Date range: {df['completedOn'].min()} to {df['completedOn'].max()}")
```

### Multi-Environment Deployment

```python
import servicepytan
import os

def get_connection(env="production"):
    """Get connection for specified environment"""
    
    if env == "production":
        return servicepytan.auth.servicepytan_connect(
            api_environment="production",
            config_file="./prod_config.json"
        )
    elif env == "integration":
        return servicepytan.auth.servicepytan_connect(
            api_environment="integration",
            config_file="./test_config.json"
        )
    else:
        raise ValueError(f"Unknown environment: {env}")

# Use environment variable to control which environment to use
current_env = os.getenv("SERVICEPYTAN_ENV", "production")
conn = get_connection(current_env)

# Your application logic here
data_service = servicepytan.DataService(conn=conn)
jobs = data_service.get_jobs_completed_between("2024-01-01", "2024-01-31")

print(f"Using {current_env} environment: {len(jobs)} jobs found")
```

## Performance Tips

### Optimize Pagination

```python
# Good: Use appropriate page sizes
options = {"pageSize": 200}  # Balance between API calls and memory
jobs = endpoint.get_all(options)

# Avoid: Very small page sizes (too many API calls)
# options = {"pageSize": 10}

# Avoid: Very large page sizes (may timeout or use too much memory)
# options = {"pageSize": 1000}
```

### Use Specific Filters

```python
# Good: Use specific filters to reduce data transfer
options = {
    "jobStatus": "Completed",
    "completedOnOrAfter": "2024-01-01T00:00:00Z",
    "completedBefore": "2024-01-31T23:59:59Z",
    "active": "true"
}

# Avoid: Retrieving all data and filtering locally
# all_jobs = endpoint.get_all({})  # Downloads everything
# filtered_jobs = [job for job in all_jobs if job['jobStatus'] == 'Completed']
```

### Connection Reuse

```python
# Good: Reuse connection objects
conn = servicepytan.auth.servicepytan_connect()

jobs_endpoint = servicepytan.Endpoint("jpm", "jobs", conn=conn)
customers_endpoint = servicepytan.Endpoint("crm", "customers", conn=conn)
invoices_endpoint = servicepytan.Endpoint("accounting", "invoices", conn=conn)

# Avoid: Creating new connections for each endpoint
# jobs_conn = servicepytan.auth.servicepytan_connect()
# customers_conn = servicepytan.auth.servicepytan_connect()
```

---

*[Back to Configuration](./configuration.md) | [View API Reference](./servicepytan.rst)*
