# Prerequisites

Before you can use ServicePytan, you need to set up a ServiceTitan API application and obtain the necessary credentials. This guide walks you through the complete setup process.

## Overview

To use ServicePytan, you'll need:

1. **ServiceTitan Account** - Access to a ServiceTitan tenant (as customer or developer)
2. **Developer Portal Access** - Ability to create and manage API applications
3. **API Application** - A registered application in the ServiceTitan Developer Portal
4. **Credentials** - Client ID, Client Secret, App ID, App Key, and Tenant ID
5. **Python Environment** - Python 3.6+ with ServicePytan installed

## Step 1: Request Developer Access

### For ServiceTitan Customers

If you're an existing ServiceTitan customer:

1. **Email Integration Team**
   - Send request to: `integrations@servicetitan.com`
   - Include your company name and ServiceTitan account details
   - Specify that you want API access for your integration project

2. **Provide Business Case**
   - Explain your integration requirements
   - Describe the data you need to access
   - Outline expected usage patterns

### For External Developers

If you're developing integrations for ServiceTitan customers:

1. **Visit Developer Portal**
   - Go to: [https://developer.servicetitan.io/request-access/](https://developer.servicetitan.io/request-access/)

2. **Complete Developer Registration**
   - Fill out the "Developer Registration Form"
   - Provide your development company information
   - Describe your intended integration

3. **Wait for Approval**
   - ServiceTitan will review your application
   - You'll receive email confirmation once approved

## Step 2: Access Developer Portal

Once approved, access the developer portal:

1. **Navigate to Portal**
   - Go to: [https://developer.servicetitan.io/signin/](https://developer.servicetitan.io/signin/)

2. **Sign In**
   - Use your ServiceTitan credentials
   - If you're an external developer, use the credentials provided in your approval email

3. **Verify Access**
   - Ensure you can see the developer dashboard
   - Confirm your organization is listed correctly

## Step 3: Create API Application

### Application Creation

1. **Start New Application**
   - Click "Create New App" or similar button
   - This creates a new API application entry

2. **Configure Application Details**
   ```
   Application Name: "My Integration" (descriptive name)
   Organization: "Your Company Name"
   Homepage: "https://yourcompany.com" (your organization's website)
   Description: "Brief description of your integration's purpose"
   ```

3. **Set Tenant Associations**
   - Add the Tenant IDs that will use this application
   - For customers: Use your own Tenant ID
   - For developers: Add customer Tenant IDs as needed

### API Scope Configuration

**Important Security Practice:** Only request access to the endpoints you actually need.

Common scopes include:
- `jpm` - Job management (jobs, appointments, estimates)
- `crm` - Customer management (customers, locations, contacts)
- `accounting` - Financial data (invoices, payments)
- `inventory` - Equipment and materials
- `settings` - Business units, technicians, job types
- `reporting` - Custom reports access

4. **Select Required Scopes**
   - Review available API scopes
   - Check only the scopes your application requires
   - Consider future needs but avoid over-requesting

5. **Complete Application**
   - Click "Create App" or "Submit"
   - Wait for the application to be created

### Record Application Credentials

6. **Note Application Details**
   - **App ID**: Found under the application title (e.g., "12345")
   - **Application Key**: Found in application details (e.g., "ak1.example123")
   
   ⚠️ **Important**: Save these immediately as they may not be easily accessible later.

## Step 4: Authorize Application in ServiceTitan

Now authorize your application within the ServiceTitan interface:

### In ServiceTitan Desktop Application

1. **Navigate to Integration Settings**
   - Log into ServiceTitan desktop application
   - Go to: `Settings > Integrations > API Application Access`

2. **Connect New Application**
   - Click "Connect New App" button
   - Select your application from the list
   - If your app doesn't appear, ensure it was created properly in Step 3

3. **Review and Accept Permissions**
   - Verify the requested permissions match your expectations
   - Ensure only necessary scopes are requested
   - Click "Allow Access" if everything looks correct

### Record Authentication Credentials

4. **Obtain Tenant ID and Client ID**
   - **Tenant ID**: Your ServiceTitan tenant identifier (e.g., "1234567890")
   - **Client ID**: OAuth client identifier (e.g., "cid.example123")

5. **Generate Client Secret**
   - Click "Generate Secret" or similar button
   - **⚠️ CRITICAL**: Copy the Client Secret immediately
   - This is your only chance to see the full secret
   - Store it securely (password manager, secure notes, etc.)

### Client Secret Management

**Important Notes:**
- Each application can have maximum 2 active client secrets
- Secrets cannot be viewed again after initial generation
- If lost, you must generate a new secret (old one remains valid until deleted)
- Consider generating a backup secret for rotation purposes

## Step 5: Environment Setup

### Installation Requirements

Ensure you have the proper Python environment:

```bash
# Check Python version (3.6+ required)
python --version

# Install ServicePytan
pip install servicepytan

# For development/testing
pip install servicepytan[dev]
```

### Environment Configuration

Choose your preferred configuration method:

#### Option A: JSON Configuration File (Recommended for Development)

Create `servicepytan_config.json`:
```json
{
    "SERVICETITAN_CLIENT_ID": "cid.your_client_id_here",
    "SERVICETITAN_CLIENT_SECRET": "cs2.your_client_secret_here",
    "SERVICETITAN_APP_ID": "your_app_id_here",
    "SERVICETITAN_APP_KEY": "ak1.your_app_key_here", 
    "SERVICETITAN_TENANT_ID": "your_tenant_id_here",
    "SERVICETITAN_TIMEZONE": "America/New_York",
    "SERVICETITAN_API_ENVIRONMENT": "production"
}
```

**Security**: Add to `.gitignore` to prevent committing credentials.

#### Option B: Environment Variables (Recommended for Production)

```bash
# Set environment variables
export SERVICETITAN_CLIENT_ID="cid.your_client_id_here"
export SERVICETITAN_CLIENT_SECRET="cs2.your_client_secret_here"
export SERVICETITAN_APP_KEY="ak1.your_app_key_here"
export SERVICETITAN_TENANT_ID="your_tenant_id_here"
export SERVICETITAN_API_ENVIRONMENT="production"
```

## Step 6: Test Your Setup

### Basic Connection Test

Create a test script to verify your setup:

```python
import servicepytan

try:
    # Test configuration loading
    conn = servicepytan.auth.servicepytan_connect(
        config_file="servicepytan_config.json"  # or omit for env vars
    )
    print("✅ Configuration loaded successfully")
    
    # Test authentication
    token = servicepytan.auth.get_auth_token(conn)
    print("✅ Authentication successful")
    
    # Test API access
    endpoint = servicepytan.Endpoint("settings", "business-units", conn=conn)
    business_units = endpoint.get_all({"pageSize": 1})
    print("✅ API access confirmed")
    
    print("🎉 Setup completed successfully!")
    
except Exception as e:
    print(f"❌ Setup failed: {e}")
    print("Please check your credentials and configuration")
```

### Environment Testing

If available, test with the integration environment:

```python
# Test integration environment
integration_conn = servicepytan.auth.servicepytan_connect(
    api_environment="integration",
    config_file="integration_config.json"
)

# Run same tests as above
```

## Credential Management Best Practices

### Security Guidelines

1. **Never Commit Credentials**
   - Add config files to `.gitignore`
   - Use environment variables in production
   - Consider using secrets management systems

2. **Principle of Least Privilege**
   - Request only necessary API scopes
   - Regularly review application permissions
   - Remove unused applications

3. **Credential Rotation**
   - Generate backup client secrets
   - Rotate secrets regularly (quarterly recommended)
   - Monitor for unauthorized usage

4. **Access Control**
   - Limit who has access to credentials
   - Use role-based access for teams
   - Audit credential usage regularly

### Secrets Management

For production environments, consider:

- **AWS Secrets Manager**
- **Azure Key Vault**
- **HashiCorp Vault**
- **Kubernetes Secrets**

## Troubleshooting Common Issues

### Application Not Found
- Verify application was created in Developer Portal
- Check that application is associated with correct tenant
- Ensure application is published/active

### Permission Denied
- Review API scopes in Developer Portal
- Verify application authorization in ServiceTitan
- Check that tenant ID matches your ServiceTitan instance

### Authentication Failures
- Verify all credentials are copied correctly
- Check for extra spaces or characters
- Ensure Client Secret hasn't expired
- Confirm you're using the correct environment (production vs integration)

### Network Issues
- Verify internet connectivity
- Check firewall settings for API endpoints:
  - Production: `https://api.servicetitan.io`
  - Integration: `https://api-integration.servicetitan.io`
  - Auth: `https://auth.servicetitan.io` or `https://auth-integration.servicetitan.io`

## Next Steps

Once your prerequisites are complete:

1. **Review Configuration Guide**: [Configuration Documentation](./configuration.md)
2. **Try Examples**: [Examples and Use Cases](./examples.md)
3. **Explore API Reference**: [ServicePytan API Reference](./servicepytan.rst)

For deployment to production environments, see: [Deployment Guide](./deployment.md)

---

*[Back to Getting Started](./index.rst) | [Next: Configuration](./configuration.md)*
