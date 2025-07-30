from datetime import datetime, timedelta
import pytz


class TimeTools:
    """Time utility class providing various time-related functions"""

    @staticmethod
    def get_local_time() -> str:
        """Get current local time"""
        try:
            local_time = datetime.now()
            return f"Local time: {local_time.strftime('%Y-%m-%d %H:%M:%S')}"
        except Exception as e:
            return f"Error: Unable to get local time - {str(e)}"

    @staticmethod
    def get_current_time(timezone_name: str = "Asia/Shanghai") -> str:
        """Get current time for specified timezone

        Args:
            timezone_name: Timezone name, defaults to "Asia/Shanghai"
        """
        try:
            tz = pytz.timezone(timezone_name)
            current_time = datetime.now(tz)
            return f"Current time ({timezone_name}): {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        except Exception as e:
            return f"Error: Unable to get time for timezone {timezone_name} - {str(e)}"

    @staticmethod
    def convert_timezone(time_str: str, from_tz: str, to_tz: str) -> str:
        """Convert time from one timezone to another

        Args:
            time_str: Time string in format "YYYY-MM-DD HH:MM:SS"
            from_tz: Source timezone name
            to_tz: Target timezone name
        """
        try:
            # Parse time string
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

            # Set source timezone
            from_timezone = pytz.timezone(from_tz)
            dt_with_tz = from_timezone.localize(dt)

            # Convert to target timezone
            to_timezone = pytz.timezone(to_tz)
            converted_time = dt_with_tz.astimezone(to_timezone)

            return f"{time_str} ({from_tz}) → {converted_time.strftime('%Y-%m-%d %H:%M:%S %Z')} ({to_tz})"
        except Exception as e:
            return f"Error: Timezone conversion failed - {str(e)}"

    @staticmethod
    def format_time(time_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format time string

        Args:
            time_str: Time string in format "YYYY-MM-DD HH:MM:SS"
            format_str: Target format, defaults to "YYYY-MM-DD HH:MM:SS"
        """
        try:
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            formatted_time = dt.strftime(format_str)
            return f"Formatted result: {formatted_time}"
        except Exception as e:
            return f"Error: Time formatting failed - {str(e)}"

    @staticmethod
    def add_time(time_str: str, days: int = 0, hours: int = 0, minutes: int = 0) -> str:
        """Add time to specified time

        Args:
            time_str: Time string in format "YYYY-MM-DD HH:MM:SS"
            days: Number of days to add
            hours: Number of hours to add
            minutes: Number of minutes to add
        """
        try:
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            delta = timedelta(days=days, hours=hours, minutes=minutes)
            new_time = dt + delta
            return (
                f"{time_str} + {days} days {hours} hours {minutes} minutes = {new_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        except Exception as e:
            return f"Error: Time calculation failed - {str(e)}"

    @staticmethod
    def get_time_difference(time1: str, time2: str) -> str:
        """Calculate difference between two times

        Args:
            time1: First time string in format "YYYY-MM-DD HH:MM:SS"
            time2: Second time string in format "YYYY-MM-DD HH:MM:SS"
        """
        try:
            dt1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
            dt2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")

            if dt1 > dt2:
                dt1, dt2 = dt2, dt1
                time1, time2 = time2, time1

            diff = dt2 - dt1
            days = diff.days
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            return f"{time2} - {time1} = {days} days {hours} hours {minutes} minutes {seconds} seconds"
        except Exception as e:
            return f"Error: Time difference calculation failed - {str(e)}"

    @staticmethod
    def list_country_timezones(country_name: str) -> str:
        """List all timezones for a specific country

        Args:
            country_name: Country name (e.g., "China", "United States", "Japan")
        """
        try:
            # Convert country name to lowercase for case-insensitive matching
            country_lower = country_name.lower()

            # Search country names to find matching country code
            country_code = None
            for code, name in pytz.country_names.items():
                if country_lower in name.lower():
                    country_code = code
                    break

            if country_code:
                try:
                    timezones = pytz.country_timezones[country_code]
                    result = f"Timezones for {pytz.country_names[country_code]} ({country_code}):\n"
                    for i, tz in enumerate(timezones, 1):
                        # Get timezone offset
                        tz_obj = pytz.timezone(tz)
                        current_time = datetime.now(tz_obj)
                        offset = current_time.strftime("%z")
                        offset_formatted = f"UTC{offset[:3]}:{offset[3:5]}"

                        result += f"{i}. {tz} ({offset_formatted})\n"
                    result += f"\nTotal: {len(timezones)} timezone(s)"
                    return result
                except KeyError:
                    return f"No timezones found for {pytz.country_names[country_code]} ({country_code})"
            else:
                return f"Country '{country_name}' not found. Please try a different country name."

        except Exception as e:
            return f"Error: Unable to get timezones for {country_name} - {str(e)}"
