"""
Auxiliary types for SQLite
"""

from __future__ import unicode_literals
from datetime import datetime


def date_time(value):
    """
    Conversion to a Python datetime given standard SQLite datetime string format
    """
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


def nullable_int(value):
    """
    These are strings converted to int but with a handler for NoneType
    """
    if value is None:
        return value
    else:
        return int(value)