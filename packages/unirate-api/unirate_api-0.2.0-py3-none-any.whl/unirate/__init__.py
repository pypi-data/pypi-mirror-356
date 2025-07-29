"""
Unirate API Client
~~~~~~~~~~~~~~~~~

A Python client for the Unirate API - real-time and historical currency exchange rates.
"""

from .client import UnirateClient
from .exceptions import UnirateError

__version__ = "0.2.0"
__all__ = ["UnirateClient", "UnirateError"] 