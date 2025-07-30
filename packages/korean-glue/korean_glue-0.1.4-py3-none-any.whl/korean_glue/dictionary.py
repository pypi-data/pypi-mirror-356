"""Manage exception dictionary for josa selection."""

from typing import Dict, Tuple, Optional

_EXCEPTION_DICT: Dict[Tuple[str, str], str] = {}


def lookup_exception(word: str, pattern: str) -> Optional[str]:
    """Return josa from exception dictionary if present."""
    return _EXCEPTION_DICT.get((word, pattern))


def add_exception_rule(word: str, pattern: str, output: str) -> None:
    """Add a custom exception rule."""
    _EXCEPTION_DICT[(word, pattern)] = output


def remove_exception_rule(word: str, pattern: str) -> None:
    """Remove a custom exception rule."""
    _EXCEPTION_DICT.pop((word, pattern), None)


def load_user_dictionary(path: str) -> None:
    """Load rules from a JSON or YAML file."""
    # Placeholder for future implementation
    pass


def get_dictionary_entries() -> Dict[Tuple[str, str], str]:
    """Return a copy of current dictionary entries."""
    return dict(_EXCEPTION_DICT)
