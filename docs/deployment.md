# Deployment Guide

This guide covers deploying ServicePytan applications in production environments, focusing on security, reliability, and best practices for internal use.

## Production Deployment Overview

### Deployment Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Application   │────│   ServicePytan  │────│  ServiceTitan   │
│    Server       │    │    Library      │    │      API        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Configuration  │    │    Logging &    │    │   Rate Limits   │
│  & Secrets      │    │   Monitoring    │    │  & Quotas       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Components

1. **Application Layer** - Your business logic and ServicePytan integration
2. **Configuration Management** - Secure credential and environment management
3. **Monitoring & Logging** - Observability and debugging capabilities
4. **Error Handling & Retry** - Resilience against API failures
5. **Security Controls** - Secure credential storage and access controls

## Environment Configuration

### Production Environment Setup

```python
# production_config.py
import os
from servicepytan.auth import servicepytan_connect, ApiEnvironment

def get_production_connection():
    """Production connection with proper error handling"""
    try:
        return servicepytan_connect(
            # Use environment variables for production
            client_id=os.environ['SERVICETITAN_CLIENT_ID'],
            client_secret=os.environ['SERVICETITAN_CLIENT_SECRET'],
            app_key=os.environ['SERVICETITAN_APP_KEY'],
            tenant_id=os.environ['SERVICETITAN_TENANT_ID'],
            timezone=os.environ.get('SERVICETITAN_TIMEZONE', 'UTC'),
            api_environment=ApiEnvironment.PRODUCTION
        )
    except KeyError as e:
        raise EnvironmentError(f"Missing required environment variable: {e}")

def get_integration_connection():
    """Integration environment for testing"""
    return servicepytan_connect(
        client_id=os.environ['SERVICETITAN_INTEGRATION_CLIENT_ID'],
        client_secret=os.environ['SERVICETITAN_INTEGRATION_CLIENT_SECRET'],
        app_key=os.environ['SERVICETITAN_INTEGRATION_APP_KEY'],
        tenant_id=os.environ['SERVICETITAN_INTEGRATION_TENANT_ID'],
        api_environment=ApiEnvironment.INTEGRATION
    )
```

### Environment Variables

**Required Production Variables:**
```bash
# ServiceTitan Production Credentials
SERVICETITAN_CLIENT_ID=cid.production_client_id
SERVICETITAN_CLIENT_SECRET=cs2.production_client_secret
SERVICETITAN_APP_KEY=ak1.production_app_key
SERVICETITAN_TENANT_ID=production_tenant_id

# Optional Configuration
SERVICETITAN_TIMEZONE=America/New_York
SERVICETITAN_API_ENVIRONMENT=production

# Application Configuration
LOG_LEVEL=INFO
RETRY_ATTEMPTS=3
BATCH_SIZE=200
```

**Integration/Testing Variables:**
```bash
# ServiceTitan Integration Credentials  
SERVICETITAN_INTEGRATION_CLIENT_ID=cid.integration_client_id
SERVICETITAN_INTEGRATION_CLIENT_SECRET=cs2.integration_client_secret
SERVICETITAN_INTEGRATION_APP_KEY=ak1.integration_app_key
SERVICETITAN_INTEGRATION_TENANT_ID=integration_tenant_id
```

## Security Best Practices

### Credential Management

#### 1. Use Secrets Management Systems

**AWS Secrets Manager:**
```python
import boto3
import json
from botocore.exceptions import ClientError

def get_servicetitan_credentials(secret_name, region_name="us-east-1"):
    """Retrieve ServiceTitan credentials from AWS Secrets Manager"""
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])
        
        return servicepytan_connect(
            client_id=secret['SERVICETITAN_CLIENT_ID'],
            client_secret=secret['SERVICETITAN_CLIENT_SECRET'],
            app_key=secret['SERVICETITAN_APP_KEY'],
            tenant_id=secret['SERVICETITAN_TENANT_ID'],
            api_environment="production"
        )
    except ClientError as e:
        raise Exception(f"Failed to retrieve credentials: {e}")

# Usage
conn = get_servicetitan_credentials("prod/servicetitan/api")
```

**Azure Key Vault:**
```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_servicetitan_credentials_azure(vault_url):
    """Retrieve ServiceTitan credentials from Azure Key Vault"""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    
    try:
        client_id = client.get_secret("servicetitan-client-id").value
        client_secret = client.get_secret("servicetitan-client-secret").value
        app_key = client.get_secret("servicetitan-app-key").value
        tenant_id = client.get_secret("servicetitan-tenant-id").value
        
        return servicepytan_connect(
            client_id=client_id,
            client_secret=client_secret,
            app_key=app_key,
            tenant_id=tenant_id,
            api_environment="production"
        )
    except Exception as e:
        raise Exception(f"Failed to retrieve credentials: {e}")
```

#### 2. Environment Separation

```python
# config.py
import os
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Config:
    def __init__(self):
        self.environment = Environment(os.environ.get('ENVIRONMENT', 'development'))
        self.debug = self.environment != Environment.PRODUCTION
        
    def get_servicetitan_connection(self):
        if self.environment == Environment.PRODUCTION:
            return get_production_connection()
        elif self.environment == Environment.STAGING:
            return get_staging_connection()
        else:
            return get_development_connection()

# Usage
config = Config()
conn = config.get_servicetitan_connection()
```

### Access Controls

#### 1. Principle of Least Privilege

```python
class ServiceTitanService:
    """Wrapper service with role-based access"""
    
    def __init__(self, user_role, conn):
        self.conn = conn
        self.user_role = user_role
        
        # Define role permissions
        self.permissions = {
            'read_only': ['get_one', 'get_all', 'get_page'],
            'operator': ['get_one', 'get_all', 'get_page', 'patch'],
            'admin': ['get_one', 'get_all', 'get_page', 'post', 'patch', 'delete']
        }
    
    def _check_permission(self, operation):
        allowed_ops = self.permissions.get(self.user_role, [])
        if operation not in allowed_ops:
            raise PermissionError(f"Role '{self.user_role}' not allowed to perform '{operation}'")
    
    def get_jobs(self, filters=None):
        self._check_permission('get_all')
        endpoint = servicepytan.Endpoint("jpm", "jobs", conn=self.conn)
        return endpoint.get_all(filters or {})
    
    def update_job(self, job_id, data):
        self._check_permission('patch')
        endpoint = servicepytan.Endpoint("jpm", "jobs", conn=self.conn)
        return endpoint.patch(job_id, data)

# Usage
service = ServiceTitanService('read_only', conn)
jobs = service.get_jobs({'active': 'true'})
```

#### 2. API Key Rotation

```python
import datetime
import logging

class CredentialRotationService:
    def __init__(self, secrets_manager):
        self.secrets_manager = secrets_manager
        self.logger = logging.getLogger(__name__)
    
    def check_credential_age(self, secret_name):
        """Check if credentials need rotation"""
        metadata = self.secrets_manager.describe_secret(SecretId=secret_name)
        last_changed = metadata['LastChangedDate']
        age_days = (datetime.datetime.now(tz=last_changed.tzinfo) - last_changed).days
        
        if age_days > 90:  # Rotate every 90 days
            self.logger.warning(f"Credentials for {secret_name} are {age_days} days old")
            return True
        return False
    
    def rotate_credentials(self, secret_name):
        """Initiate credential rotation"""
        self.logger.info(f"Starting credential rotation for {secret_name}")
        # Implement rotation logic based on your infrastructure
        pass
```

## Monitoring and Logging

### Application Logging

```python
import logging
import structlog
from datetime import datetime

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.WriteLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

class ServiceTitanLogger:
    """Enhanced logging for ServiceTitan API interactions"""
    
    def __init__(self, service_name):
        self.logger = structlog.get_logger().bind(service=service_name)
    
    def log_api_call(self, endpoint, method, params=None, duration=None, error=None):
        """Log API call details"""
        log_data = {
            'endpoint': f"{endpoint.folder}/{endpoint.endpoint}",
            'method': method,
            'timestamp': datetime.utcnow().isoformat(),
        }
        
        if params:
            log_data['params'] = params
        if duration:
            log_data['duration_ms'] = duration * 1000
        if error:
            log_data['error'] = str(error)
            self.logger.error("API call failed", **log_data)
        else:
            self.logger.info("API call successful", **log_data)

# Usage
api_logger = ServiceTitanLogger("data_sync_service")

def get_jobs_with_logging(conn, filters):
    import time
    
    endpoint = servicepytan.Endpoint("jpm", "jobs", conn=conn)
    start_time = time.time()
    
    try:
        result = endpoint.get_all(filters)
        duration = time.time() - start_time
        
        api_logger.log_api_call(
            endpoint=endpoint,
            method="get_all",
            params=filters,
            duration=duration
        )
        
        return result
        
    except Exception as e:
        duration = time.time() - start_time
        api_logger.log_api_call(
            endpoint=endpoint,
            method="get_all",
            params=filters,
            duration=duration,
            error=e
        )
        raise
```

### Performance Monitoring

```python
import time
from functools import wraps
from dataclasses import dataclass
from typing import Dict, List
import statistics

@dataclass
class APIMetrics:
    endpoint: str
    call_count: int
    total_duration: float
    avg_duration: float
    error_count: int
    success_rate: float

class PerformanceMonitor:
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
        self.errors: Dict[str, int] = {}
        self.calls: Dict[str, int] = {}
    
    def record_call(self, endpoint, duration, success=True):
        """Record API call metrics"""
        key = f"{endpoint.folder}/{endpoint.endpoint}"
        
        if key not in self.metrics:
            self.metrics[key] = []
            self.errors[key] = 0
            self.calls[key] = 0
        
        self.metrics[key].append(duration)
        self.calls[key] += 1
        
        if not success:
            self.errors[key] += 1
    
    def get_metrics(self) -> Dict[str, APIMetrics]:
        """Get aggregated metrics"""
        result = {}
        
        for endpoint, durations in self.metrics.items():
            if durations:
                avg_duration = statistics.mean(durations)
                total_duration = sum(durations)
                call_count = self.calls[endpoint]
                error_count = self.errors[endpoint]
                success_rate = (call_count - error_count) / call_count if call_count > 0 else 0
                
                result[endpoint] = APIMetrics(
                    endpoint=endpoint,
                    call_count=call_count,
                    total_duration=total_duration,
                    avg_duration=avg_duration,
                    error_count=error_count,
                    success_rate=success_rate
                )
        
        return result

# Global monitor instance
monitor = PerformanceMonitor()

def monitored_api_call(func):
    """Decorator to monitor API calls"""
    @wraps(func)
    def wrapper(endpoint, *args, **kwargs):
        start_time = time.time()
        success = True
        
        try:
            result = func(endpoint, *args, **kwargs)
            return result
        except Exception as e:
            success = False
            raise
        finally:
            duration = time.time() - start_time
            monitor.record_call(endpoint, duration, success)
    
    return wrapper

# Apply to ServicePytan methods
servicepytan.Endpoint.get_all = monitored_api_call(servicepytan.Endpoint.get_all)
servicepytan.Endpoint.get_one = monitored_api_call(servicepytan.Endpoint.get_one)
```

## Error Handling and Resilience

### Retry Strategies

```python
import time
import random
from functools import wraps
from requests.exceptions import RequestException, Timeout, ConnectionError

class RetryConfig:
    def __init__(self, max_attempts=3, base_delay=1, max_delay=60, backoff_factor=2):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor

def retry_with_backoff(config: RetryConfig = None):
    """Retry decorator with exponential backoff and jitter"""
    if config is None:
        config = RetryConfig()
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(config.max_attempts):
                try:
                    return func(*args, **kwargs)
                
                except (ConnectionError, Timeout, RequestException) as e:
                    last_exception = e
                    
                    if attempt == config.max_attempts - 1:
                        logger.error(f"Max retry attempts reached for {func.__name__}")
                        raise
                    
                    # Calculate delay with exponential backoff and jitter
                    delay = min(
                        config.base_delay * (config.backoff_factor ** attempt),
                        config.max_delay
                    )
                    jitter = random.uniform(0, 0.1) * delay
                    total_delay = delay + jitter
                    
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}, "
                        f"retrying in {total_delay:.2f} seconds: {e}"
                    )
                    time.sleep(total_delay)
            
            raise last_exception
        
        return wrapper
    return decorator

# Apply retry logic to ServicePytan calls
class ResilientServiceTitanClient:
    def __init__(self, conn, retry_config=None):
        self.conn = conn
        self.retry_config = retry_config or RetryConfig()
    
    @retry_with_backoff()
    def get_jobs(self, filters):
        endpoint = servicepytan.Endpoint("jpm", "jobs", conn=self.conn)
        return endpoint.get_all(filters)
    
    @retry_with_backoff()
    def get_customers(self, filters):
        endpoint = servicepytan.Endpoint("crm", "customers", conn=self.conn)
        return endpoint.get_all(filters)
```

### Circuit Breaker Pattern

```python
import time
from enum import Enum
from threading import Lock

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60, reset_timeout=30):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.reset_timeout = reset_timeout
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._lock = Lock()
    
    def call(self, func, *args, **kwargs):
        with self._lock:
            if self.state == CircuitState.OPEN:
                if time.time() - self.last_failure_time > self.reset_timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.failure_count = 0
                else:
                    raise Exception("Circuit breaker is OPEN")
            
            try:
                result = func(*args, **kwargs)
                
                if self.state == CircuitState.HALF_OPEN:
                    self.state = CircuitState.CLOSED
                
                self.failure_count = 0
                return result
                
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = CircuitState.OPEN
                
                raise

# Usage
circuit_breaker = CircuitBreaker(failure_threshold=3, reset_timeout=60)

def protected_api_call(endpoint, method, *args, **kwargs):
    """API call protected by circuit breaker"""
    return circuit_breaker.call(getattr(endpoint, method), *args, **kwargs)
```

## Deployment Patterns

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python health_check.py

EXPOSE 8000

CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  servicepytan-app:
    build: .
    environment:
      - ENVIRONMENT=production
      - SERVICETITAN_CLIENT_ID=${SERVICETITAN_CLIENT_ID}
      - SERVICETITAN_CLIENT_SECRET=${SERVICETITAN_CLIENT_SECRET}
      - SERVICETITAN_APP_KEY=${SERVICETITAN_APP_KEY}
      - SERVICETITAN_TENANT_ID=${SERVICETITAN_TENANT_ID}
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "health_check.py"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: servicepytan-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: servicepytan-app
  template:
    metadata:
      labels:
        app: servicepytan-app
    spec:
      containers:
      - name: servicepytan-app
        image: your-registry/servicepytan-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: SERVICETITAN_CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: servicetitan-secrets
              key: client-id
        - name: SERVICETITAN_CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: servicetitan-secrets
              key: client-secret
        - name: SERVICETITAN_APP_KEY
          valueFrom:
            secretKeyRef:
              name: servicetitan-secrets
              key: app-key
        - name: SERVICETITAN_TENANT_ID
          valueFrom:
            secretKeyRef:
              name: servicetitan-secrets
              key: tenant-id
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Secret
metadata:
  name: servicetitan-secrets
  namespace: production
type: Opaque
data:
  client-id: <base64-encoded-client-id>
  client-secret: <base64-encoded-client-secret>
  app-key: <base64-encoded-app-key>
  tenant-id: <base64-encoded-tenant-id>
```

## Performance Optimization

### Connection Pooling

```python
from threading import Lock
from queue import Queue
import threading

class ConnectionPool:
    def __init__(self, max_connections=10):
        self.max_connections = max_connections
        self.pool = Queue(maxsize=max_connections)
        self.created_connections = 0
        self.lock = Lock()
    
    def get_connection(self):
        """Get connection from pool or create new one"""
        try:
            # Try to get existing connection
            return self.pool.get_nowait()
        except:
            # Create new connection if pool is empty
            with self.lock:
                if self.created_connections < self.max_connections:
                    conn = servicepytan.auth.servicepytan_connect()
                    self.created_connections += 1
                    return conn
                else:
                    # Wait for available connection
                    return self.pool.get()
    
    def return_connection(self, conn):
        """Return connection to pool"""
        try:
            self.pool.put_nowait(conn)
        except:
            # Pool is full, discard connection
            pass

# Global connection pool
connection_pool = ConnectionPool(max_connections=5)

class PooledServiceTitanClient:
    def __init__(self):
        self.local = threading.local()
    
    def _get_connection(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = connection_pool.get_connection()
        return self.local.conn
    
    def get_jobs(self, filters):
        conn = self._get_connection()
        endpoint = servicepytan.Endpoint("jpm", "jobs", conn=conn)
        return endpoint.get_all(filters)
```

### Caching Strategy

```python
import redis
import json
import hashlib
from datetime import datetime, timedelta

class ServiceTitanCache:
    def __init__(self, redis_url="redis://localhost:6379/0"):
        self.redis_client = redis.from_url(redis_url)
        self.default_ttl = 3600  # 1 hour
    
    def _generate_key(self, endpoint, method, params):
        """Generate cache key from request parameters"""
        key_data = f"{endpoint.folder}/{endpoint.endpoint}/{method}/{json.dumps(params, sort_keys=True)}"
        return f"servicepytan:{hashlib.md5(key_data.encode()).hexdigest()}"
    
    def get(self, endpoint, method, params):
        """Get cached response"""
        key = self._generate_key(endpoint, method, params)
        cached_data = self.redis_client.get(key)
        
        if cached_data:
            return json.loads(cached_data)
        return None
    
    def set(self, endpoint, method, params, data, ttl=None):
        """Cache response data"""
        key = self._generate_key(endpoint, method, params)
        ttl = ttl or self.default_ttl
        
        self.redis_client.setex(
            key,
            ttl,
            json.dumps(data, default=str)
        )

# Usage with caching
cache = ServiceTitanCache()

def cached_api_call(endpoint, method, params, cache_ttl=3600):
    """API call with caching"""
    # Try cache first
    cached_result = cache.get(endpoint, method, params)
    if cached_result:
        logger.info(f"Cache hit for {endpoint.folder}/{endpoint.endpoint}")
        return cached_result
    
    # Make API call
    result = getattr(endpoint, method)(params)
    
    # Cache result
    cache.set(endpoint, method, params, result, cache_ttl)
    logger.info(f"Cached result for {endpoint.folder}/{endpoint.endpoint}")
    
    return result
```

## Health Checks and Monitoring

### Application Health Check

```python
# health_check.py
import sys
import time
import logging
from datetime import datetime, timedelta

def check_servicetitan_connection():
    """Check ServiceTitan API connectivity"""
    try:
        conn = servicepytan.auth.servicepytan_connect()
        endpoint = servicepytan.Endpoint("settings", "business-units", conn=conn)
        
        start_time = time.time()
        result = endpoint.get_all({"pageSize": 1})
        response_time = time.time() - start_time
        
        return {
            "status": "healthy",
            "response_time_ms": response_time * 1000,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

def check_credentials_age():
    """Check if credentials are approaching expiration"""
    # Implement based on your credential management system
    return {"status": "healthy", "days_until_expiration": 45}

def health_check():
    """Comprehensive health check"""
    checks = {
        "servicetitan_api": check_servicetitan_connection(),
        "credentials": check_credentials_age(),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    overall_status = "healthy" if all(
        check["status"] == "healthy" 
        for check in checks.values() 
        if isinstance(check, dict) and "status" in check
    ) else "unhealthy"
    
    checks["overall_status"] = overall_status
    return checks

if __name__ == "__main__":
    result = health_check()
    print(json.dumps(result, indent=2))
    
    if result["overall_status"] != "healthy":
        sys.exit(1)
```

## Deployment Checklist

### Pre-deployment

- [ ] **Security Review**
  - [ ] Credentials stored securely (not in code)
  - [ ] API permissions reviewed and minimized
  - [ ] Access controls implemented
  - [ ] Secrets rotation schedule established

- [ ] **Environment Setup**
  - [ ] Production environment variables configured
  - [ ] Integration environment available for testing
  - [ ] Network access to ServiceTitan API confirmed
  - [ ] DNS resolution working

- [ ] **Monitoring Setup**
  - [ ] Logging configured and tested
  - [ ] Health checks implemented
  - [ ] Performance monitoring enabled
  - [ ] Alert thresholds defined

### Post-deployment

- [ ] **Validation**
  - [ ] Health checks passing
  - [ ] API connectivity confirmed
  - [ ] Authentication working
  - [ ] Sample data retrieved successfully

- [ ] **Monitoring**
  - [ ] Logs flowing correctly
  - [ ] Metrics being collected
  - [ ] Alerts configured
  - [ ] Dashboard created

- [ ] **Documentation**
  - [ ] Deployment procedures documented
  - [ ] Troubleshooting runbook created
  - [ ] Contact information updated
  - [ ] Credential rotation procedures documented

---

*[Back to Troubleshooting](./troubleshooting.md) | [Back to Getting Started](./index.rst)*