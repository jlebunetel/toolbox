"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the 'context_processors' option of the configuration
of a DjangoTemplates backend and used by RequestContext.
"""

from django.http import HttpRequest

from toolbox import __version__


def version(request: HttpRequest) -> dict[str, str]:  # noqa: V107
    """Context processor that provides the version of the current project."""
    return {"version": __version__}
