class MemryError(Exception):
    """Base exception for the Memry client."""
    pass

class ConnectionError(MemryError):
    """Raised when the client cannot connect to the Memry daemon."""
    pass

class ServerError(MemryError):
    """Raised when the server returns an error message."""
    pass