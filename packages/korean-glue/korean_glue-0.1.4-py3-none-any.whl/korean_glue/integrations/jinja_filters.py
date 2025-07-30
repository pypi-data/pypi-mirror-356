"""Jinja2 filters for korean_glue."""

from jinja2 import Environment

from ..engine import attach


def josa_filter(word, pattern):
    if not isinstance(word, str):
        return word
    return attach(word, pattern)


def register(env: Environment) -> None:
    env.filters["josa"] = josa_filter
