from datetime import datetime, timedelta

import pytz
from django.utils import timezone


class TimeDeltaMixin:
    """Mixin for timedelta."""

    def get_timedelta_hours(self, time_delta: timedelta) -> int:
        """Get timedelta in hours as int."""
        try:
            total_seconds = time_delta.total_seconds()
            hours = total_seconds // 3600
            return hours
        except Exception as exc:
            raise exc

    def get_timedelta_minutes(self, time_delta: timedelta) -> int:
        """Get normalized timedelta in minutes as int after extracting hours."""
        try:
            total_seconds = time_delta.total_seconds()
            hours, remaining_seconds = divmod(total_seconds, 3600)
            minutes = remaining_seconds // 60

            return minutes
        except Exception as exc:
            raise exc

    def get_timedelta_seconds(self, time_delta: timedelta) -> int:
        """Get normalized duraion remaining seconds as int after extracting hours and minutes."""
        try:
            total_seconds = time_delta.total_seconds()
            hours, remaining_seconds = divmod(total_seconds, 3600)
            minutes, normalized_seconds = divmod(remaining_seconds, 60)

            return normalized_seconds
        except Exception:
            return

    def get_readable_timedelta_string(self, time_delta: timedelta) -> str:
        """Return timedelta in human readable alloted time format.

        Formatted in h hrs, m minutes.
        """
        try:

            hours = int(self.get_timedelta_hours(time_delta))
            minutes = int(self.get_timedelta_minutes(time_delta))
            seconds = int(self.get_timedelta_seconds(time_delta))

            hour_string = "hour" if hours == 1 else "hours"
            minute_string = "min" if minutes == 1 else "mins"
            seconds_string = "sec" if seconds == 1 else "secs"

            readable_time_delta = ""

            if hours > 0:
                readable_time_delta += f"{hours} {hour_string}"

                if minutes > 0:
                    readable_time_delta += f", {minutes} {minute_string}"

                if seconds > 0:
                    readable_time_delta += f", {seconds} {seconds_string}"
            else:
                if minutes > 0:
                    readable_time_delta += f"{minutes} {minute_string}"

                    if seconds > 0:
                        readable_time_delta += f", {seconds} {seconds_string}"
                else:
                    readable_time_delta += f"{seconds} {seconds_string}"

            return readable_time_delta
        except Exception as exc:
            raise exc


class DateTimeMixin(TimeDeltaMixin):
    """Date and time mixin."""

    def get_datetime_string_with_timezone(
        self, datetime_obj: datetime, short=False
    ) -> str:
        """Get the datetime string with timezone in this format:

        May 28, 2022 02:00:08 PM AEST+1000

        if short is True
        May 28, 2022 02:00 PM AEST
        """
        datetime_format = "%B %d, %Y %I:%M:%S %p %Z%z"
        if short:
            datetime_format = "%B %d, %Y %I:%M %p %Z"

        return datetime_obj.strftime(datetime_format)

    def get_current_melbourne_datetime(self) -> datetime:
        """Return current melbourne datetime."""
        melbourne_timezone = pytz.timezone("Australia/Melbourne")
        server_datetime = timezone.now()
        melbourne_datetime = server_datetime.astimezone(melbourne_timezone)

        return melbourne_datetime

    def get_current_melbourne_year(self) -> int:
        """Get the current year in melbourne."""
        melbourne_datetime = self.get_current_melbourne_datetime()
        return melbourne_datetime.year

    def get_javascript_date_string(self, date: datetime.date) -> str:
        """Get html <input type='date'>  accepted string format of date object.

        Accepted format:
        `%Y-%m-%d`
        """

        string_format = "%Y-%m-%d"

        return date.strftime(string_format)

    def get_javascript_time_string(self, time: datetime.time) -> str:
        """Get html <input type='time'>  accepted string format of time object.

        Accepted format:
        `%H:%M`
        """

        string_format = "%H:%M"
        return time.strftime(string_format)


datetime_mixin = DateTimeMixin()
