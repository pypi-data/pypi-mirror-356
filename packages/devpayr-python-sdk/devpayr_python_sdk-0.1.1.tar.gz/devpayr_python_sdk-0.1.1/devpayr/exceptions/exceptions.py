class DevPayrException(Exception):
    """
    Base exception class for all DevPayr SDK errors.
    """
    def __init__(self, message: str):
        super().__init__(f"[DevPayr] {message}")


class InvalidLicenseException(DevPayrException):
    """
    Raised when a license key is invalid or unverified.
    """
    pass


class UnauthorizedException(DevPayrException):
    """
    Raised when API access is unauthorized.
    """
    pass


class ConfigurationException(DevPayrException):
    """
    Raised when configuration is missing or malformed.
    """
    pass


class HttpRequestException(DevPayrException):
    """
    Raised when a remote HTTP request fails or times out.
    """
    def __init__(self, status_code: int, message: str = "HTTP request failed"):
        self.status_code = status_code
        super().__init__(f"{message} (status code: {status_code})")


class InjectableVerificationException(DevPayrException):
    """
    Raised when an injectable fails signature verification.
    """
    pass


class CryptoException(DevPayrException):
    """
    Raised when an injectable fails signature verification.
    """
    pass