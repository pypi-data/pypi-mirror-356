"""Custom exceptions for korean_glue."""


class JosaError(Exception):
    """Base error for josa processing."""


class DictionaryError(JosaError):
    """Raised when there is a problem with the dictionary."""
