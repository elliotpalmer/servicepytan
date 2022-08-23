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
  """Parse date string to datetime object"""
  return parse(date_string)

def _change_timezones(datetime_object, timezone):
    """Convert a datetime object from one timezone to UTC"""
    timezone = pytz.timezone(timezone)
    parsed_date = timezone.localize(datetime_object)
    parsed_date = _convert_datetime_to_utc(parsed_date)
    return parsed_date

def _format_date_to_iso_format(datetime_object):
  """Format datetime object to ISO format"""
  return datetime_object.strftime('%Y-%m-%dT%H:%M:%SZ')

def _convert_datetime_to_utc(datetime_object):
  """Convert datetime object to UTC"""
  return datetime_object.astimezone(pytz.UTC)