"""Core engine handling particle attachment."""

from .rules import select_josa
from .dictionary import lookup_exception


def attach(word: str, pattern: str) -> str:
    """Attach the proper josa to ``word`` according to ``pattern``."""
    josa = get_josa(word, pattern)
    return f"{word}{josa}"


def get_josa(word: str, pattern: str) -> str:
    """Return the correct josa for ``word`` and ``pattern``."""
    josa = lookup_exception(word, pattern)
    if josa is not None:
        return josa
    return select_josa(word, pattern)
