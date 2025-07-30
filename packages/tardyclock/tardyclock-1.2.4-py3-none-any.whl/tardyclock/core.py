from datetime import datetime
from random import choice
import pytz


def random_time(hr24: bool = True, showtimezone: bool = False):
  """Tells you the current time in a timezone of its choosing"""
  tz = pytz.timezone(choice(pytz.all_timezones))
  now = datetime.now(tz)

  time_format = f"%A %B %m, %Y, {'%H' if hr24 else '%I'}:%M:%S"
  if showtimezone:
    time_format += " %Z"

  return now.strftime(time_format)
