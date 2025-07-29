class UnirateError(Exception):
    """Base exception for all Unirate client errors."""
    pass

class AuthenticationError(UnirateError):
    """Raised when there are authentication issues."""
    pass

class RateLimitError(UnirateError):
    """Raised when API rate limits are exceeded."""
    pass

class InvalidCurrencyError(UnirateError):
    """Raised when an invalid currency code is provided."""
    pass

class InvalidDateError(UnirateError):
    """Raised when an invalid date format is provided."""
    pass

class APIError(UnirateError):
    """Raised when the API returns an error response."""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response 