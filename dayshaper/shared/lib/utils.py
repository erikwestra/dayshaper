""" dayshaper.shared.lib.utils

    This module provides various utility functions for the Dayshaper system.
"""
import datetime

from django.utils import timezone

#############################################################################

def current_datetime():
    """ Return the current date and time.

        We return a datetime.datetime object representing the current date and
        time.
    """
    return datetime.datetime.now().replace(microsecond=0)

#############################################################################

def start_of_day():
    """ Return the start of the current day.

        We return a datetime.datetime object representing "midnight last
        night".
    """
    now = current_datetime()
    return datetime.datetime(now.year, now.month, now.day)

#############################################################################

def start_of_week():
    """ Return the start of the current week.

        We return a datetime.datetime object representing "midnight on the most
        recent Monday".
    """
    timestamp = start_of_day()
    while timestamp.date().weekday() != 0:
        timestamp = timestamp - datetime.timedelta(days=1)
    return timestamp

#############################################################################

def datetime_to_seconds(dt):
    """ Convert a datetime.datetime object into an integer number of seconds.
    """
    epoch = datetime.datetime(1970, 1, 1)
    delta = dt - epoch
    return (delta.days*24*3600) + delta.seconds

#############################################################################

def seconds_to_datetime(secs):
    """ Convert an integer number of secs back into a datetime.datetime object.
    """
    epoch = datetime.datetime(1970, 1, 1)
    delta = datetime.timedelta(seconds=secs)
    timestamp = epoch + delta
    return timestamp

#############################################################################

def format_seconds_for_display(seconds):
    """ Format the given number of seconds for display.

        We return a string containing a human-readable representation of the
        given number of seconds.  For example, if "seconds" is 60, we return
        "1 minute".
    """
    days = seconds / 86400
    seconds = seconds - 86400 * days

    hours = seconds / 3600
    seconds = seconds - 3600 * hours

    minutes = seconds / 60
    seconds = seconds - 60 * minutes

    parts = []
    if days != 0:
        if days == 1:
            parts.append("1 day")
        else:
            parts.append("%s days" % days)

    if hours != 0:
        if hours == 1:
            parts.append("1 hour")
        else:
            parts.append("%s hours" % hours)
    elif len(parts) > 0:
        parts.append("0 hours")

    if minutes != 0:
        if minutes == 1:
            parts.append("1 minute")
        else:
            parts.append("%s minutes" % minutes)
    elif len(parts) > 0:
        parts.append("0 minutes")

    if seconds == 1:
        parts.append("1 second")
    else:
        parts.append("%s seconds" % seconds)

    if len(parts) == 1:
        return parts[0]
    else:
        return ", ".join(parts[:-1]) + " and " + parts[-1]

