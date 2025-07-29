import unittest
from datetime import datetime
import pytz
from servicepytan._dates import (
    _convert_date_to_api_format,
    _parse_date_string,
    _change_timezones,
    _format_date_to_iso_format,
    _convert_datetime_to_utc,
)


class TestDates(unittest.TestCase):
    def test_convert_date_to_api_format_with_string(self):
        self.assertEqual(
            _convert_date_to_api_format("2024-01-01 12:00:00"),
            "2024-01-01T12:00:00Z",
        )

    def test_convert_date_to_api_format_with_string_and_timezone(self):
        # Test with a timezone that is not in DST
        self.assertEqual(
            _convert_date_to_api_format(
                "2024-01-01 12:00:00", "America/New_York"
            ),
            "2024-01-01T17:00:00Z",  # EST is UTC-5
        )
        # Test with a timezone that is in DST
        self.assertEqual(
            _convert_date_to_api_format(
                "2024-07-01 12:00:00", "America/New_York"
            ),
            "2024-07-01T16:00:00Z",  # EDT is UTC-4
        )

    def test_convert_date_to_api_format_with_datetime(self):
        dt = datetime(2024, 1, 1, 12, 0, 0)
        self.assertEqual(
            _convert_date_to_api_format(dt), "2024-01-01T12:00:00Z"
        )

    def test_convert_date_to_api_format_with_datetime_and_timezone(self):
        dt = datetime(2024, 1, 1, 12, 0, 0)
        # Test with a timezone that is not in DST
        self.assertEqual(
            _convert_date_to_api_format(dt, "America/New_York"),
            "2024-01-01T17:00:00Z",  # EST is UTC-5
        )
        # Test with a timezone that is in DST
        dt_dst = datetime(2024, 7, 1, 12, 0, 0)
        self.assertEqual(
            _convert_date_to_api_format(dt_dst, "America/New_York"),
            "2024-07-01T16:00:00Z",  # EDT is UTC-4
        )

    def test_parse_date_string(self):
        self.assertEqual(
            _parse_date_string("2024-01-01 12:00:00"),
            datetime(2024, 1, 1, 12, 0, 0),
        )

    def test_change_timezones(self):
        dt = datetime(2024, 1, 1, 12, 0, 0)
        utc_dt = _change_timezones(dt, "America/New_York")
        self.assertEqual(utc_dt.tzinfo, pytz.UTC)
        self.assertEqual(utc_dt.hour, 17)

    def test_format_date_to_iso_format(self):
        dt = datetime(2024, 1, 1, 12, 0, 0)
        self.assertEqual(
            _format_date_to_iso_format(dt), "2024-01-01T12:00:00Z"
        )

    def test_convert_datetime_to_utc(self):
        est = pytz.timezone("America/New_York")
        dt = est.localize(datetime(2024, 1, 1, 12, 0, 0))
        utc_dt = _convert_datetime_to_utc(dt)
        self.assertEqual(utc_dt.tzinfo, pytz.UTC)
        self.assertEqual(utc_dt.hour, 17)


if __name__ == "__main__":
    unittest.main()
