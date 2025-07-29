#!/usr/bin/env python

import logging
from datetime import datetime


########################################################################################################################

def now():
    """Returns current time and date: <year>-<month>-<day> <hour>:<minute>:<second>.<microsecond>

    Returns
    -------
    datetime.datetime object
    """
    return datetime.now()


def set_timestamp(s, date_format=None):
    """Returns a date object of a string in format %Y-%m-%d.

    Parameters
    ----------
    s : str
        The date in string format
    date_format : str
        The expected format of the date string format.
        Please refer to https://strftime.org/

    Returns
    -------
    ts : datetime.datetime object
        If the provided string ('s') parameter is not in valid format, None is returned.
    """

    if not date_format:
        date_format = "%Y-%m-%d"
    try:
        ts = datetime.strptime(str(s), date_format)
    except ValueError:
        logging.error(f"Unable to convert provided argument '{str(s)}' to timestamp object")
        return

    return ts

