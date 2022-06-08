from xml.dom import ValidationErr
from django.test import TestCase
from .forms import ProductForm

class TestProductForm(TestCase):

    def test_form_valid(self):
        """
        Confirm that the form validates successfully.
        """
        data = {
            "name": "test product",
            "brand": "test brand",
            "colour": "test colour",
            "size": 1,
            "paint_type": "OL",
            "cost_price": "4.99",
            "retail_price": "9.99",
            "inventory_count": "10"
        }

        form = ProductForm(data)
        self.assertTrue(form.is_valid())

    def test_inventory_count_validation_error(self):
        """
        Confirm that the form throws appropriate validation
        error message if no inventory count value specified.
        """
        data = {
            "name": "test product",
            "brand": "test brand",
            "colour": "test colour",
            "size": 1,
            "paint_type": "OL",
            "cost_price": "4.99",
            "retail_price": "9.99",
            "inventory_count": "0"
        }

        form = ProductForm(data)
        error_message = ("* No amount of inventory units specified."
                " Please enter the amount of units to add.")
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["__all__"].as_text(), error_message)
