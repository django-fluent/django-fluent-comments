from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase
from fluent_comments.utils import import_symbol


class UtilTestCase(SimpleTestCase):
    """
    Testing import_symbol
    """

    def test_import_symbol_errors(self):
        self.assertRaises(ImproperlyConfigured, lambda: import_symbol("fluent_comments.FooBar", "FOOBAR"))
        self.assertRaises(ImproperlyConfigured, lambda: import_symbol("fluent_comments_na.FooBar", "FOOBAR"))
