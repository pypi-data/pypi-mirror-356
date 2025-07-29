"""Django template filters for korean_glue."""

from django import template

from ..engine import attach

register = template.Library()


@register.filter(name="josa")
def josa_filter(word, pattern):
    if not isinstance(word, str):
        return word
    return attach(word, pattern)
