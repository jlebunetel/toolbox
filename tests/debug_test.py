"""A simple debug test module."""

from django.test import TestCase


class DebugTestCase(TestCase):
    """A simple debug test class."""

    def test_debug(self) -> None:
        """A simple debug test."""
        self.assertTrue(not False)
