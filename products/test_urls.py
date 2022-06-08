from ast import Add
from django.test import TestCase
from django.urls import reverse, resolve

from .views import AddProductView


class TestProductUrls(TestCase):
    """
    Unit Tests for Product URLs
    """

    def test_resolution_for_add_product_view(self):
        """
        Confirm that the URL to add_product_view is correctly configured
        to display the appropriate view.
        """
        resolver = resolve(reverse("add_product"))
        self.assertEquals(
            resolver.func.__name__, AddProductView.as_view().__name__)