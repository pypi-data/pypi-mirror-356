"""
NSE Socket Client Library
A professional Python client library for the NSE Socket server with WebSocket and REST API support.
"""

from .nse_client import (
    NSEClient,
    NSESocketError,
    AuthenticationError,
    ConnectionError,
    SubscriptionError,
    HistoricalDataError,
    AdminError,
    get_token,
    create_client
)

__version__ = "0.5"
__author__ = "siddid"

__all__ = [
    "NSEClient",
    "NSESocketError", 
    "AuthenticationError",
    "ConnectionError",
    "SubscriptionError", 
    "HistoricalDataError",
    "AdminError",
    "get_token",
    "create_client"
] 