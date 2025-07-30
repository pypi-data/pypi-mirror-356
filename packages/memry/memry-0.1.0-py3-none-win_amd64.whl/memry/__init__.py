"""
Memry: Lightning-fast, in-memory, cross-process data frames for Python.
Stop Pickling. Start Computing.
"""
__version__ = "0.1.0"

# --- CORRECTED IMPORTS ---
# We no longer import `start_server` from `memry.server` because that
# function has been removed. The user now starts the server via the command line.
# We also no longer need to import `shutdown_server` here, as it's not part of the primary API.

from .client import put, get, delete, list_keys, close, shutdown_server
from .exceptions import MemryError, ConnectionError, ServerError