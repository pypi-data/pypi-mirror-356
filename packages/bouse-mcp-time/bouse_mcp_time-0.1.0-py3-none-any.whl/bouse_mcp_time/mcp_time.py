from fastmcp import FastMCP
from .time_tools import TimeTools

# Initialize FastMCP server
mcp = FastMCP("time")


@mcp.tool()
def get_local_time() -> str:
    """Get the current local time."""
    return TimeTools.get_local_time()


@mcp.tool()
def get_current_time(timezone_name: str = "Asia/Shanghai") -> str:
    """Get the current time in the specified timezone.

    Args:
        timezone_name: Timezone name, defaults to "Asia/Shanghai"
    """
    return TimeTools.get_current_time(timezone_name)


@mcp.tool()
def convert_timezone(time_str: str, from_tz: str, to_tz: str) -> str:
    """Convert time from one timezone to another.

    Args:
        time_str: Time string in format "YYYY-MM-DD HH:MM:SS"
        from_tz: Source timezone name
        to_tz: Target timezone name
    """
    return TimeTools.convert_timezone(time_str, from_tz, to_tz)


@mcp.tool()
def format_time(time_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a time string.

    Args:
        time_str: Time string in format "YYYY-MM-DD HH:MM:SS"
        format_str: Target format, defaults to "YYYY-MM-DD HH:MM:SS"
    """
    return TimeTools.format_time(time_str, format_str)


@mcp.tool()
def add_time(time_str: str, days: int = 0, hours: int = 0, minutes: int = 0) -> str:
    """Add time to a specified time.

    Args:
        time_str: Time string in format "YYYY-MM-DD HH:MM:SS"
        days: Number of days to add
        hours: Number of hours to add
        minutes: Number of minutes to add
    """
    return TimeTools.add_time(time_str, days, hours, minutes)


@mcp.tool()
def get_time_difference(time1: str, time2: str) -> str:
    """Calculate the difference between two times.

    Args:
        time1: First time string in format "YYYY-MM-DD HH:MM:SS"
        time2: Second time string in format "YYYY-MM-DD HH:MM:SS"
    """
    return TimeTools.get_time_difference(time1, time2)


@mcp.tool()
def list_country_timezones(country_name: str) -> str:
    """List all timezones for a specific country.

    Args:
        country_name: Country name (e.g., "China", "United States", "Japan")
    """
    return TimeTools.list_country_timezones(country_name)


if __name__ == "__main__":
    # This runs the server, defaulting to STDIO transport
    # mcp.run()

    # To use a different transport, e.g., HTTP:
    mcp.run(transport="sse", host="0.0.0.0", port=9000, path="/sse")
    # mcp.run(transport="streamable-http", host="127.0.0.1", port=9000, path="/mcp")
