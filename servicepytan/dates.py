from dateutil.parser import parse
import pytz

def convert_date_to_api_format(date, timezone=""):
  # 
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
  return parse(date_string)

def _change_timezones(datetime_object, timezone):
    timezone = pytz.timezone(timezone)
    parsed_date = timezone.localize(datetime_object)
    parsed_date = _convert_datetime_to_utc(parsed_date)
    return parsed_date

def _format_date_to_iso_format(datetime_object):
  return datetime_object.strftime('%Y-%m-%dT%H:%M:%SZ')

def _convert_datetime_to_utc(datetime_object):
  return datetime_object.astimezone(pytz.UTC)