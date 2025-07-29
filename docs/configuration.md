# Configuration

ServicePytan offers multiple flexible configuration methods to accommodate different development and deployment scenarios. Choose the method that best fits your use case.

## Configuration Methods

### 1. JSON Configuration File (Recommended for Development)

Create a JSON configuration file containing your ServiceTitan API credentials:

```json
{
    "SERVICETITAN_CLIENT_ID": "cid.your_client_id_here",
    "SERVICETITAN_CLIENT_SECRET": "cs2.your_client_secret_here",
    "SERVICETITAN_APP_ID": "your_app_id_here",
    "SERVICETITAN_APP_KEY": "ak1.your_app_key_here",
    "SERVICETITAN_TENANT_ID": "1234567890",
    "SERVICETITAN_TIMEZONE": "America/New_York",
    "SERVICETITAN_API_ENVIRONMENT": "production"
}
```

**Usage:**
```python
import servicepytan

conn = servicepytan.auth.servicepytan_connect(
    config_file="./servicepytan_config.json"
)
```

**Security Note:** Always exclude configuration files from version control by adding them to your `.gitignore`:
```
servicepytan_config.json
*.json
```

### 2. Environment Variables (Recommended for Production)

Set environment variables in your deployment environment or `.env` file:

```bash
# Required credentials
export SERVICETITAN_CLIENT_ID="cid.your_client_id_here"
export SERVICETITAN_CLIENT_SECRET="cs2.your_client_secret_here"
export SERVICETITAN_APP_KEY="ak1.your_app_key_here"
export SERVICETITAN_TENANT_ID="1234567890"

# Optional configuration
export SERVICETITAN_APP_ID="your_app_id_here"
export SERVICETITAN_TIMEZONE="America/New_York"
export SERVICETITAN_API_ENVIRONMENT="production"
```

**Using .env file:**
Create a `.env` file in your project root:
```env
SERVICETITAN_CLIENT_ID=cid.your_client_id_here
SERVICETITAN_CLIENT_SECRET=cs2.your_client_secret_here
SERVICETITAN_APP_KEY=ak1.your_app_key_here
SERVICETITAN_TENANT_ID=1234567890
SERVICETITAN_TIMEZONE=America/New_York
SERVICETITAN_API_ENVIRONMENT=production
```

**Usage:**
```python
import servicepytan

# ServicePytan automatically loads from environment variables
conn = servicepytan.auth.servicepytan_connect()
```

### 3. Direct Parameters (For Dynamic Configuration)

Pass credentials directly to the connection function:

```python
import servicepytan

conn = servicepytan.auth.servicepytan_connect(
    client_id="cid.your_client_id_here",
    client_secret="cs2.your_client_secret_here",
    app_key="ak1.your_app_key_here",
    tenant_id="1234567890",
    timezone="America/New_York",
    api_environment="production"
)
```

## Configuration Parameters

### Required Parameters

| Parameter | Description | Where to Find |
|-----------|-------------|---------------|
| `SERVICETITAN_CLIENT_ID` | OAuth Client ID | ServiceTitan: Settings > Integrations > API Application Access > [App Name] > Edit |
| `SERVICETITAN_CLIENT_SECRET` | OAuth Client Secret | Generated once with Client ID (store securely) |
| `SERVICETITAN_APP_KEY` | Application Key | ServiceTitan Developer Portal > App Definition |
| `SERVICETITAN_TENANT_ID` | Your ServiceTitan Tenant ID | ServiceTitan Developer Portal > App Definition |

### Optional Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `SERVICETITAN_APP_ID` | Application ID | `None` | Found in Developer Portal |
| `SERVICETITAN_TIMEZONE` | Timezone for date operations | `"UTC"` | Any timezone from [TimeZone DB](https://timezonedb.com/time-zones) |
| `SERVICETITAN_API_ENVIRONMENT` | API Environment | `"production"` | `"production"` or `"integration"` |

## Environment Support

ServicePytan supports both ServiceTitan API environments:

### Production Environment (Default)
- **Auth URL:** `https://auth.servicetitan.io`
- **API URL:** `https://api.servicetitan.io`
- **Use for:** Live data, production applications

### Integration Environment
- **Auth URL:** `https://auth-integration.servicetitan.io`
- **API URL:** `https://api-integration.servicetitan.io`
- **Use for:** Development, testing, staging

**Switch environments:**
```python
# Production (default)
conn = servicepytan.auth.servicepytan_connect(
    api_environment="production"
)

# Integration/Testing
conn = servicepytan.auth.servicepytan_connect(
    api_environment="integration"
)
```

## Timezone Configuration

ServicePytan handles timezone conversions automatically. Specify your timezone to ensure accurate date/time operations:

```python
# Common timezone examples
conn = servicepytan.auth.servicepytan_connect(
    timezone="America/New_York"      # Eastern Time
    # timezone="America/Chicago"     # Central Time
    # timezone="America/Denver"      # Mountain Time
    # timezone="America/Los_Angeles" # Pacific Time
    # timezone="UTC"                 # UTC (default)
)
```

**Supported formats:**
- IANA timezone names (recommended): `"America/New_York"`
- Standard abbreviations: `"EST"`, `"PST"`, etc.
- Full timezone list: https://timezonedb.com/time-zones

## Configuration Priority

ServicePytan uses the following priority order for configuration:

1. **Direct parameters** passed to `servicepytan_connect()`
2. **JSON configuration file** (if `config_file` parameter provided)
3. **Environment variables** (loaded automatically)

Higher priority options override lower priority ones.

## Security Best Practices

### Development
- ✅ Use JSON config files excluded from version control
- ✅ Use `.env` files for local development
- ❌ Never commit credentials to version control

### Production
- ✅ Use environment variables
- ✅ Use secrets management systems (AWS Secrets Manager, Azure Key Vault, etc.)
- ✅ Rotate credentials regularly
- ❌ Never store credentials in code

### General
- ✅ Use least-privilege API applications
- ✅ Monitor API usage and access logs
- ✅ Use HTTPS-only environments
- ✅ Validate credentials before deployment

## Troubleshooting Configuration

### Common Issues

**"Authentication Failed" Errors:**
1. Verify credentials are correct and up-to-date
2. Check if API application is active in ServiceTitan
3. Ensure correct environment (production vs integration)
4. Validate tenant ID matches your ServiceTitan instance

**Environment Variable Not Found:**
1. Check variable names match exactly (case-sensitive)
2. Restart your application after setting variables
3. Verify `.env` file is in the correct location
4. Ensure no trailing spaces in variable values

**Timezone Issues:**
1. Use IANA timezone names for best compatibility
2. Check timezone spelling and capitalization
3. Default to "UTC" if unsure

### Validation Example

Test your configuration:

```python
import servicepytan

try:
    conn = servicepytan.auth.servicepytan_connect()
    
    # Test authentication
    token = servicepytan.auth.get_auth_token(conn)
    print("✅ Authentication successful!")
    
    # Test API access
    test_endpoint = servicepytan.Endpoint("jpm", "jobs", conn=conn)
    jobs = test_endpoint.get_all({"pageSize": 1})
    print("✅ API access successful!")
    
except Exception as e:
    print(f"❌ Configuration error: {e}")
```

---

*[Back to Getting Started](./index.rst) | [View Examples](./examples.md)*
