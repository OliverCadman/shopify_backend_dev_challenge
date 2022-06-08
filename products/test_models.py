from django.test import TestCase
from .models import Product


class TestProductModels(TestCase):
    """
    Unit tests for Product model.
    """

    def test_product_created(self):
        """
        Confirm that a single product is added to the test database,
        and that the field values for the product object match the ones
        passed in upon creation.
        """
        test_product = Product.objects.create(
            name="test product",
            brand="test brand",
            colour="test colour",
            paint_type="WC",
            size=2,
            cost_price=14.55,
            retail_price=25.99
        )

        self.assertEqual(len(Product.objects.all()), 1)
        self.assertEqual(test_product.colour, "test colour")
        self.assertEqual(test_product.__str__(), "test product")
        self.assertEqual(test_product.paint_type, "WC")
        self.assertEqual(test_product.size, 2)
        self.assertEqual(test_product.sku, "TB-TC-WC-2")
        self.assertEqual(test_product.cost_price, 14.55)
        self.assertEqual(test_product.retail_price, 25.99)
        
    
    def test_sku_created_with_single_word(self):
        """
        Confirm that a brand name SKU is created 
        when one word is passed into the 'brand' string field.
        """
        test_product = Product.objects.create(
            name="test product",
            brand="brand",
            colour="test colour",
            paint_type="WC",
            size=2,
            cost_price=14.55,
            retail_price=25.99
        )

        self.assertEqual(test_product.sku, "BRA-TC-WC-2")
    
    def test_sku_created_with_multiple_words(self):
        """
        Confirm that the brand name SKU is created
        when multiple words are passed into the 'brand' string field.
        """
        test_product = Product.objects.create(
            name="test product",
            brand="another test brand for django",
            colour="test colour",
            paint_type="WC",
            size=2,
            cost_price=14.55,
            retail_price=25.99
        )

        self.assertEqual(test_product.sku, "ATBFD-TC-WC-2")
    
    def test_sku_created_with_single_word_containing_three_characters(self):
        test_product = Product.objects.create(
            name="test product",
            brand="tes",
            colour="test colour",
            paint_type="WC",
            size=2,
            cost_price=14.55,
            retail_price=25.99
        )

        self.assertEqual(test_product.sku, "TES-TC-WC-2")

    
    def test_product_creation_with_numbers(self):
        test_product = Product.objects.create(
            name="1",
            brand="2",
            colour="3",
            paint_type="4",
            size=2,
            cost_price=14.55,
            retail_price=25.99
        )
        print(test_product.sku)
        self.assertEqual(len(Product.objects.all()), 1)


