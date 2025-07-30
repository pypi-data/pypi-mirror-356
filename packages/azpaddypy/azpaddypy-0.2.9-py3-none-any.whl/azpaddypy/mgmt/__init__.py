"""
AzPaddyPy - A standardized Python package for Azure cloud services integration.
"""

__version__ = "0.1.0"

from azpaddypy.mgmt.logging import AzureLogger
from azpaddypy.mgmt.identity import AzureIdentity

__all__ = [
    "AzureLogger", 
    "AzureIdentity",
]
