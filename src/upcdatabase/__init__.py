"""UPC Database Python Library

A Python library for accessing the UPC Database API.
Access product information, search capabilities, and more.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

from .client import UPCDatabase, UPCDatabaseError

__all__ = ["UPCDatabase", "UPCDatabaseError"]
