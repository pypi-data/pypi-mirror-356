"""
Unirate API Client
~~~~~~~~~~~~~~~~~

A Python client for the Unirate API - real-time and historical currency exchange rates.
"""

from .client import UnirateClient
from .exceptions import UnirateError

__version__ = "1.0.0"
__all__ = ["UnirateClient", "UnirateError"] 