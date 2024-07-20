"""Utility functions."""

import time
import datetime


def now(time_format: str = "iso8061") -> str:
    """Return current timestamp in given format.

    Args:
        time_format (str, optional): Timestamp format. Defaults to "iso8061".
        - `iso8061`: yyyy-MM-ddTHH:mm:ss (KST).
        - `epoch`  : e.g., "1721492171.951993"
    """
    return (
        datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        if time_format == "iso8061"
        else str(time.time())
    )
