"""Dates Module: Converting Dates to UTC format"""

from dateutil.parser import parse
import pytz

def _convert_date_to_api_format(date, timezone=""):
  """Converts a date into ISO format compatible with API endpoint parameters.

  The function will either format the date as is if no timezone is provided or convert to UTC from
  the timezone parameter. The function accepts BOTH a string that it will try to parse into a 
  datetime object. If a datetime object is also acceptable.

  Args:
      date: A string or datetime object
      timezone: A string using a Timezone DB abbreviation (e.g. 'America/New_York' = Eastern Time)

  Returns:
      A date string in ISO format
  """  
  # Checks the date string for format and parses if not date object
  if isinstance(date, str):
    parsed_date = _parse_date_string(date)
  else:
    parsed_date = date
  
  # If no timezone is provided then assume it is provided in UTC
  # Otherwise, perform the conversion from the stated TZ to UTC
  if timezone != "":
    parsed_date = _change_timezones(parsed_date, timezone)

  formatted_date = _format_date_to_iso_format(parsed_date)
  return formatted_date

def _parse_date_string(date_string):
  """Parse date string to datetime object.
  
  Uses dateutil.parser to intelligently parse various date string formats
  into a datetime object. This handles most common date formats automatically.
  
  Args:
      date_string: String representation of a date/time
      
  Returns:
      datetime: Parsed datetime object
      
  Raises:
      ValueError: If the date string cannot be parsed
      
  Examples:
      >>> _parse_date_string("2024-01-15")
      >>> _parse_date_string("January 15, 2024")
      >>> _parse_date_string("2024-01-15T10:30:00")
  """
  return parse(date_string)

def _change_timezones(datetime_object, timezone):
    """Convert a datetime object from one timezone to UTC.
    
    Takes a naive datetime object (without timezone info) and treats it as
    being in the specified timezone, then converts it to UTC.
    
    Args:
        datetime_object: Naive datetime object to convert
        timezone: Source timezone string (e.g., "America/New_York")
        
    Returns:
        datetime: UTC datetime object with timezone information
        
    Examples:
        >>> dt = datetime(2024, 1, 15, 10, 30)  # 10:30 AM
        >>> utc_dt = _change_timezones(dt, "America/New_York")
        >>> # Returns equivalent UTC time (15:30 in winter, 14:30 in summer)
    """
    timezone = pytz.timezone(timezone)
    parsed_date = timezone.localize(datetime_object)
    parsed_date = _convert_datetime_to_utc(parsed_date)
    return parsed_date

def _format_date_to_iso_format(datetime_object):
  """Format datetime object to ISO format string.
  
  Converts a datetime object to the ISO 8601 format string required
  by the ServiceTitan API endpoints.
  
  Args:
      datetime_object: Datetime object to format
      
  Returns:
      str: ISO format date string (YYYY-MM-DDTHH:MM:SSZ)
      
  Examples:
      >>> dt = datetime(2024, 1, 15, 10, 30, 45)
      >>> _format_date_to_iso_format(dt)
      >>> # Returns: "2024-01-15T10:30:45Z"
  """
  return datetime_object.strftime('%Y-%m-%dT%H:%M:%SZ')

def _convert_datetime_to_utc(datetime_object):
  """Convert datetime object to UTC timezone.
  
  Converts a timezone-aware datetime object to UTC timezone.
  This is used as the final step in timezone conversion.
  
  Args:
      datetime_object: Timezone-aware datetime object
      
  Returns:
      datetime: Datetime object converted to UTC timezone
      
  Examples:
      >>> est = pytz.timezone('America/New_York')
      >>> dt = est.localize(datetime(2024, 1, 15, 10, 30))
      >>> utc_dt = _convert_datetime_to_utc(dt)
      >>> # Returns datetime in UTC (15:30)
  """
  return datetime_object.astimezone(pytz.UTC)