#!/usr/bin/env python

"""Console script for servicepytan."""
import sys
import click
import json
from typing import Optional

from servicepytan.auth import servicepytan_connect, get_auth_headers
from servicepytan.requests import Endpoint
from servicepytan.data import DataService
from servicepytan.utils import create_credential_file


@click.group()
@click.version_option()
def main():
    """ServicePytan CLI - Command line interface for ServiceTitan API interactions."""
    pass


@main.command()
@click.option('--config-file', '-c', help='Path to configuration file')
@click.option('--output', '-o', default='servicepytan_config.json', help='Output configuration file name')
def init(config_file: Optional[str], output: str):
    """Initialize ServicePytan configuration."""
    if config_file:
        click.echo(f"Using existing config file: {config_file}")
    else:
        config_path = create_credential_file(output)
        click.echo(f"Created configuration template: {config_path}")
        click.echo("\nPlease edit the configuration file with your ServiceTitan credentials:")
        click.echo("- SERVICETITAN_CLIENT_ID")
        click.echo("- SERVICETITAN_CLIENT_SECRET") 
        click.echo("- SERVICETITAN_APP_KEY")
        click.echo("- SERVICETITAN_TENANT_ID")
        click.echo("- SERVICETITAN_API_ENVIRONMENT (production or integration)")


@main.command()
@click.option('--config-file', '-c', help='Path to configuration file')
@click.option('--environment', '-e', default='production', help='API environment (production or integration)')
def test_connection(config_file: Optional[str], environment: str):
    """Test connection to ServiceTitan API."""
    try:
        if config_file:
            conn = servicepytan_connect(config_file=config_file)
        else:
            conn = servicepytan_connect(api_environment=environment)
        
        # Test authentication
        headers = get_auth_headers(conn)
        click.echo("✅ Authentication successful!")
        click.echo(f"Environment: {conn.get('SERVICETITAN_API_ENVIRONMENT', 'unknown')}")
        click.echo(f"Tenant ID: {conn.get('SERVICETITAN_TENANT_ID', 'unknown')}")
        
    except Exception as e:
        click.echo(f"❌ Connection failed: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option('--config-file', '-c', help='Path to configuration file')
@click.option('--folder', '-f', required=True, help='API folder (e.g., jpm, sales, inventory)')
@click.option('--endpoint', '-e', required=True, help='API endpoint (e.g., jobs, estimates)')
@click.option('--id', help='Specific record ID to retrieve')
@click.option('--modifier', help='Endpoint modifier (e.g., notes, attachments)')
@click.option('--limit', '-l', default=10, help='Limit number of results (default: 10)')
@click.option('--output-format', '-of', default='json', type=click.Choice(['json', 'table']), help='Output format')
def get(config_file: Optional[str], folder: str, endpoint: str, id: Optional[str], 
        modifier: Optional[str], limit: int, output_format: str):
    """Get data from ServiceTitan API endpoint."""
    try:
        if config_file:
            conn = servicepytan_connect(config_file=config_file)
        else:
            conn = servicepytan_connect()
        
        api_endpoint = Endpoint(folder, endpoint, conn)
        
        if id:
            # Get specific record
            data = api_endpoint.get_one(id=id, modifier=modifier or "")
            click.echo(json.dumps(data, indent=2))
        else:
            # Get multiple records
            query = {"pageSize": limit}
            data = api_endpoint.get_many(query=query, modifier=modifier or "")
            
            if output_format == 'json':
                click.echo(json.dumps(data, indent=2))
            else:
                # Simple table format
                if 'data' in data and data['data']:
                    records = data['data']
                    if records:
                        # Print headers
                        headers = list(records[0].keys())
                        click.echo('\t'.join(headers))
                        
                        # Print data rows
                        for record in records:
                            values = [str(record.get(h, '')) for h in headers]
                            click.echo('\t'.join(values))
                else:
                    click.echo("No data found")
                    
    except Exception as e:
        click.echo(f"❌ Request failed: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option('--config-file', '-c', help='Path to configuration file')
@click.option('--start-date', '-s', required=True, help='Start date (YYYY-MM-DD)')
@click.option('--end-date', '-e', required=True, help='End date (YYYY-MM-DD)')
@click.option('--job-status', multiple=True, default=['Completed'], help='Job status filter (can be used multiple times)')
@click.option('--output-format', '-of', default='json', type=click.Choice(['json', 'csv']), help='Output format')
def jobs(config_file: Optional[str], start_date: str, end_date: str, job_status: tuple, output_format: str):
    """Get jobs data for a date range using DataService."""
    try:
        if config_file:
            conn = servicepytan_connect(config_file=config_file)
        else:
            conn = servicepytan_connect()
        
        data_service = DataService(conn)
        jobs_data = data_service.get_jobs_completed_between(
            start_date, end_date, list(job_status)
        )
        
        if output_format == 'json':
            click.echo(json.dumps(jobs_data, indent=2))
        else:
            # CSV format
            if jobs_data:
                import csv
                import sys
                
                fieldnames = jobs_data[0].keys()
                writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(jobs_data)
            else:
                click.echo("No jobs found for the specified criteria")
                
    except Exception as e:
        click.echo(f"❌ Request failed: {str(e)}", err=True)
        sys.exit(1)


@main.command()
def list_endpoints():
    """List common ServiceTitan API endpoints."""
    endpoints = {
        "Job Planning & Management": {
            "jobs": "Job records and details",
            "appointments": "Scheduled appointments", 
            "job-types": "Job type configurations"
        },
        "Sales": {
            "estimates": "Sales estimates",
            "customers": "Customer information"
        },
        "Inventory": {
            "purchase-orders": "Purchase order records",
            "items": "Inventory items"
        },
        "Settings": {
            "employees": "Employee records",
            "technicians": "Technician information",
            "business-units": "Business unit configurations"
        }
    }
    
    for folder, items in endpoints.items():
        click.echo(f"\n📁 {folder}:")
        for endpoint, description in items.items():
            click.echo(f"  • {endpoint}: {description}")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover