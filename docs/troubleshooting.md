# Troubleshooting

This guide helps you resolve common issues when using ServicePytan with the ServiceTitan API.

## Authentication Issues

### "Invalid Client Credentials" Error

**Problem:** Authentication fails with invalid credentials error.

**Solutions:**
1. **Verify Credentials:**
   ```python
   import servicepytan
   
   # Check your configuration
   conn = servicepytan.auth.servicepytan_connect(config_file="./config.json")
   print("Client ID:", conn.get('SERVICETITAN_CLIENT_ID', 'Not set'))
   print("Tenant ID:", conn.get('SERVICETITAN_TENANT_ID', 'Not set'))
   # Never print secrets in production!
   ```

2. **Check Credential Sources:**
   - Ensure `CLIENT_ID` and `CLIENT_SECRET` match in ServiceTitan
   - Verify `APP_KEY` and `TENANT_ID` are correct
   - Check if API application is active in ServiceTitan

3. **Validate Environment:**
   ```python
   # Ensure you're using the correct environment
   conn = servicepytan.auth.servicepytan_connect(
       api_environment="production"  # or "integration"
   )
   ```

### "Application Not Found" Error

**Problem:** API returns application not found error.

**Solutions:**
1. Verify `APP_ID` and `APP_KEY` in Developer Portal
2. Ensure API application is published and active
3. Check tenant association in ServiceTitan settings

### Environment Variable Issues

**Problem:** Environment variables not loading correctly.

**Solutions:**
1. **Check Variable Names:**
   ```bash
   # Verify environment variables are set
   echo $SERVICETITAN_CLIENT_ID
   echo $SERVICETITAN_TENANT_ID
   ```

2. **Use .env File:**
   ```bash
   # Create .env file in project root
   cat > .env << EOF
   SERVICETITAN_CLIENT_ID=your_client_id
   SERVICETITAN_CLIENT_SECRET=your_client_secret
   SERVICETITAN_APP_KEY=your_app_key
   SERVICETITAN_TENANT_ID=your_tenant_id
   EOF
   ```

3. **Manual Loading:**
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   print("Variables loaded:", bool(os.getenv('SERVICETITAN_CLIENT_ID')))
   ```

## API Request Issues

### "Rate Limit Exceeded" Error

**Problem:** API returns 429 rate limit errors.

**Solutions:**
1. **Implement Retry Logic:**
   ```python
   import time
   import servicepytan
   
   def safe_api_call(endpoint, options, max_retries=3):
       for attempt in range(max_retries):
           try:
               return endpoint.get_all(options)
           except requests.HTTPError as e:
               if e.response.status_code == 429:
                   wait_time = 2 ** attempt  # Exponential backoff
                   print(f"Rate limited, waiting {wait_time} seconds...")
                   time.sleep(wait_time)
               else:
                   raise
       raise Exception("Max retries exceeded")
   ```

2. **Reduce Request Frequency:**
   - Increase page sizes (up to 500 for most endpoints)
   - Add delays between requests
   - Use caching for repeated data

### "Request Timeout" Error

**Problem:** API requests timeout before completing.

**Solutions:**
1. **Reduce Page Size:**
   ```python
   # Instead of large pages
   options = {"pageSize": 50}  # Smaller, more reliable
   ```

2. **Add Request Timeouts:**
   ```python
   import requests
   
   # Custom timeout handling
   try:
       data = endpoint.get_all(options)
   except requests.Timeout:
       print("Request timed out, trying smaller batch...")
   ```

3. **Break Into Smaller Date Ranges:**
   ```python
   # Instead of large date ranges
   jobs = data_service.get_jobs_completed_between(
       "2024-01-01", "2024-01-07"  # Weekly chunks
   )
   ```

### "Permission Denied" Error

**Problem:** API returns 403 permission denied errors.

**Solutions:**
1. **Check API Application Permissions:**
   - Verify endpoint access in ServiceTitan Developer Portal
   - Ensure required scopes are granted

2. **Validate Tenant Access:**
   ```python
   # Test basic access
   endpoint = servicepytan.Endpoint("settings", "business-units", conn=conn)
   business_units = endpoint.get_all({"pageSize": 1})
   print("Access confirmed:", len(business_units) >= 0)
   ```

3. **Review Integration Settings:**
   - Check if integration is active
   - Verify correct tenant association

## Data Issues

### Empty Results When Data Expected

**Problem:** API returns empty results when data should exist.

**Solutions:**
1. **Check Date Formats:**
   ```python
   # Ensure correct timezone and format
   from datetime import datetime
   import pytz
   
   # Convert to UTC for API
   local_date = datetime(2024, 1, 1)
   utc_date = pytz.timezone('America/New_York').localize(local_date).astimezone(pytz.UTC)
   formatted_date = utc_date.strftime("%Y-%m-%dT%H:%M:%SZ")
   ```

2. **Verify Filter Parameters:**
   ```python
   # Debug filters step by step
   options = {"pageSize": 10}  # Start simple
   all_jobs = endpoint.get_all(options)
   print(f"Total jobs without filters: {len(all_jobs)}")
   
   # Add filters gradually
   options["jobStatus"] = "Completed"
   filtered_jobs = endpoint.get_all(options)
   print(f"Completed jobs: {len(filtered_jobs)}")
   ```

3. **Check Environment Data:**
   ```python
   # Ensure you're checking the right environment
   print(f"Using environment: {conn.get('SERVICETITAN_API_ENVIRONMENT')}")
   print(f"API Root: {conn.get('api_root')}")
   ```

### Incorrect Date/Time Data

**Problem:** Date and time values appear incorrect.

**Solutions:**
1. **Configure Timezone:**
   ```python
   conn = servicepytan.auth.servicepytan_connect(
       timezone="America/New_York"  # Set your local timezone
   )
   ```

2. **Parse Dates Correctly:**
   ```python
   from datetime import datetime
   import pytz
   
   # Parse ServiceTitan date strings
   def parse_st_date(date_string, local_tz="America/New_York"):
       utc_date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
       local_tz = pytz.timezone(local_tz)
       return utc_date.astimezone(local_tz)
   ```

## Performance Issues

### Slow API Responses

**Problem:** API requests take too long to complete.

**Solutions:**
1. **Optimize Page Sizes:**
   ```python
   # Find optimal page size for your use case
   page_sizes = [50, 100, 200, 500]
   for size in page_sizes:
       start_time = time.time()
       options = {"pageSize": size}
       result = endpoint.get_page(options, page=1)
       duration = time.time() - start_time
       print(f"Page size {size}: {duration:.2f}s for {len(result['data'])} records")
   ```

2. **Use Specific Filters:**
   ```python
   # More specific filters = faster responses
   options = {
       "pageSize": 200,
       "active": "true",
       "jobStatus": "Completed",
       "completedOnOrAfter": "2024-01-01T00:00:00Z"
   }
   ```

3. **Parallel Processing:**
   ```python
   from concurrent.futures import ThreadPoolExecutor
   
   def get_jobs_by_status(status):
       endpoint = servicepytan.Endpoint("jpm", "jobs", conn=conn)
       return endpoint.get_all({"jobStatus": status})
   
   statuses = ["Completed", "Scheduled", "InProgress"]
   with ThreadPoolExecutor(max_workers=3) as executor:
       results = list(executor.map(get_jobs_by_status, statuses))
   ```

### Memory Usage Issues

**Problem:** Application uses too much memory with large datasets.

**Solutions:**
1. **Process in Chunks:**
   ```python
   def process_jobs_in_chunks(start_date, end_date, chunk_size=1000):
       page = 1
       while True:
           options = {
               "pageSize": chunk_size,
               "page": page,
               "completedOnOrAfter": start_date,
               "completedBefore": end_date
           }
           
           chunk = endpoint.get_page(options, page=page)
           if not chunk['data']:
               break
               
           # Process chunk immediately
           yield chunk['data']
           page += 1
   
   for job_chunk in process_jobs_in_chunks("2024-01-01", "2024-12-31"):
       # Process each chunk
       for job in job_chunk:
           # Do something with job
           pass
   ```

2. **Use Generators:**
   ```python
   def stream_jobs(options):
       page = 1
       while True:
           page_options = {**options, "page": page}
           result = endpoint.get_page(page_options, page=page)
           
           for job in result['data']:
               yield job
               
           if len(result['data']) < options.get('pageSize', 50):
               break
           page += 1
   
   # Memory-efficient processing
   for job in stream_jobs({"jobStatus": "Completed"}):
       print(job['id'])
   ```

## Reports Issues

### "Report Not Found" Error

**Problem:** Cannot access custom reports.

**Solutions:**
1. **Verify Report ID:**
   ```python
   from servicepytan.reports import get_report_list
   
   # List available reports
   reports = get_report_list("operations", conn=conn)
   for report in reports['data']:
       print(f"{report['name']}: {report['id']}")
   ```

2. **Check Report Category:**
   ```python
   from servicepytan.reports import get_report_categories
   
   categories = get_report_categories(conn=conn)
   for category in categories['data']:
       print(f"Category: {category['name']}")
   ```

### Report Parameters Validation

**Problem:** Report parameters are rejected.

**Solutions:**
1. **Check Parameter Types:**
   ```python
   report = servicepytan.Report("operations", "report_id", conn=conn)
   
   # Show required parameters
   report.show_param_types()
   
   # Get parameter metadata
   print(report.metadata.get('parameters', []))
   ```

2. **Validate Dynamic Sets:**
   ```python
   from servicepytan.reports import get_dynamic_set_list
   
   # Get valid values for dynamic parameters
   business_units = get_dynamic_set_list("business-units", conn=conn)
   print("Valid business unit IDs:", [unit[0] for unit in business_units])
   ```

## Development Environment Setup

### Module Import Issues

**Problem:** Cannot import servicepytan modules.

**Solutions:**
1. **Verify Installation:**
   ```bash
   pip list | grep servicepytan
   pip install --upgrade servicepytan
   ```

2. **Check Python Path:**
   ```python
   import sys
   print("Python path:", sys.path)
   
   try:
       import servicepytan
       print("ServicePytan version:", servicepytan.__version__)
   except ImportError as e:
       print("Import error:", e)
   ```

3. **Virtual Environment:**
   ```bash
   # Create clean environment
   python -m venv venv_servicepytan
   source venv_servicepytan/bin/activate  # Linux/Mac
   # or venv_servicepytan\Scripts\activate  # Windows
   
   pip install servicepytan
   ```

### Dependency Conflicts

**Problem:** Package dependency conflicts.

**Solutions:**
1. **Check Dependencies:**
   ```bash
   pip check
   pip list --outdated
   ```

2. **Install Specific Versions:**
   ```bash
   # Create requirements.txt with specific versions
   pip freeze > requirements.txt
   
   # Or install specific version
   pip install servicepytan==0.3.2
   ```

## Debugging Tips

### Enable Verbose Logging

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('servicepytan')
logger.setLevel(logging.DEBUG)

# Now all API requests will be logged
conn = servicepytan.auth.servicepytan_connect()
```

### Test Connection

```python
def test_servicepytan_connection():
    """Comprehensive connection test"""
    try:
        # Test authentication
        conn = servicepytan.auth.servicepytan_connect()
        print("✅ Configuration loaded")
        
        # Test token retrieval
        token = servicepytan.auth.get_auth_token(conn)
        print("✅ Authentication successful")
        
        # Test API access
        endpoint = servicepytan.Endpoint("settings", "business-units", conn=conn)
        data = endpoint.get_all({"pageSize": 1})
        print("✅ API access confirmed")
        
        # Test DataService
        data_service = servicepytan.DataService(conn=conn)
        print("✅ DataService initialized")
        
        print("🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

test_servicepytan_connection()
```

### API Response Inspection

```python
def debug_api_response(endpoint, options):
    """Debug API responses step by step"""
    import json
    
    print(f"Testing endpoint: {endpoint.folder}/{endpoint.endpoint}")
    print(f"Options: {json.dumps(options, indent=2)}")
    
    try:
        # Test single page first
        response = endpoint.get_page(options, page=1)
        print(f"✅ Page 1: {len(response.get('data', []))} records")
        print(f"Total pages: {response.get('totalPages', 'unknown')}")
        print(f"Total count: {response.get('totalCount', 'unknown')}")
        
        if response.get('data'):
            print("Sample record keys:", list(response['data'][0].keys()))
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

# Usage
conn = servicepytan.auth.servicepytan_connect()
endpoint = servicepytan.Endpoint("jpm", "jobs", conn=conn)
debug_api_response(endpoint, {"pageSize": 5, "active": "true"})
```

## Getting Help

If you can't resolve your issue:

1. **Check the GitHub Issues:** https://github.com/elliotpalmer/servicepytan/issues
2. **ServiceTitan Developer Docs:** https://developer.servicetitan.io/
3. **Create a New Issue:** Include:
   - ServicePytan version
   - Python version
   - Complete error message
   - Minimal code example
   - Expected vs actual behavior

---

*[Back to Examples](./examples.md) | [Back to Getting Started](./index.rst)*