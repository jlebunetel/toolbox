"""Test templates module"""

from django.test import TestCase
from django.test.client import RequestFactory

from templates.context_processors import version
from toolbox import __version__


class ContextProcessorsTestCase(TestCase):
    """Context processors test case"""

    def setUp(self) -> None:
        self.rf = RequestFactory()

    def test_version(self) -> None:
        """Context processors returns the current version"""
        context: dict[str, str] = version(request=self.rf.get("/"))
        self.assertEqual(context["version"], __version__)
