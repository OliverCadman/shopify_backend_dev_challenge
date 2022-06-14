from cgi import test
from django.test import TestCase
from .models import Shipment, ShipmentLineItem
from products.models import Product
from .test_utils import calculate_test_total


class ShipmentModelTest(TestCase):

    def setUp(self):
        """
        Create Shipment object, along with Product and ShipmentLineItem
        objects to use as related objects.
        """


        # Create shipment
        self.test_shipment = Shipment.objects.create(
            recipient_name="test name",
            email="test@email.com",
            phone_number="01234567890",
            country="GB",
            postcode="W11NX",
            street_address1="test street address 1",
            street_address2="test street address 2",
            county="test county",
            status=1
        )

        # Confirm that all appropriate fields are added successfully.
        self.assertEqual(len(Shipment.objects.all()), 1)
        self.assertEqual(self.test_shipment.recipient_name, "test name")
        self.assertEqual(self.test_shipment.email, "test@email.com")
        self.assertEqual(self.test_shipment.phone_number, "01234567890")
        self.assertEqual(self.test_shipment.country.name, "United Kingdom")
        self.assertEqual(self.test_shipment.postcode, "W11NX")
        self.assertEqual(self.test_shipment.street_address1, "test street address 1")
        self.assertEqual(self.test_shipment.street_address2, "test street address 2")
        self.assertEqual(self.test_shipment.county, "test county")
        self.assertEqual(self.test_shipment.status, 1)

        # Create Test Products
        self.test_product1 = Product.objects.create(
            name="test product 1",
            brand="test brand 1",
            colour="test colour 1",
            paint_type="OL",
            size=1,
            cost_price=2.99,
            retail_price=6.99,
            inventory_count=50
        )

        self.test_product2 = Product.objects.create(
            name="test product 2",
            brand="test brand 2",
            colour="test colour 2",
            paint_type="WC",
            size=1,
            cost_price=2.99,
            retail_price=6.99,
            inventory_count=50
        )

        # Create test ShipmentLineItems
        self.shipment_line_item1 = ShipmentLineItem.objects.create(
            shipment=self.test_shipment,
            product=self.test_product1,
            quantity=10,
        )

        self.shipment_line_item2 = ShipmentLineItem.objects.create(
            shipment=self.test_shipment,
            product=self.test_product2,
            quantity=10,
        )

        # Decrement test_product's inventory count by quantity specified in 
        # shipment_line_item creation
        self.test_product1.decrement_inventory_count(self.shipment_line_item1.quantity)

        self.test_product2.decrement_inventory_count(self.shipment_line_item2.quantity)

    def test_calculate_cost_price_total(self):
        """
        Confirm the ShipmentLineItems calculate_costprice_total method
        returns the correct value.
        """

        # Calculate control cost_price
        total_cost_control = calculate_test_total(
            self.shipment_line_item1.product.cost_price,
            self.shipment_line_item1.quantity)
            
        # Invoke calculate_costprice_total method of ShipmentLineItem object
        total_cost_test = round(
            self.shipment_line_item1.calculate_costprice_total(), 2)

        # Confirm the control and test calculations match.
        self.assertEqual(total_cost_control, total_cost_test)
    
    def test_calculate_retail_price_total(self):
        """
        Confirm the ShipmentLineItems calculate_retailprice_total method
        returns the correct value.
        """

        total_retail_control = calculate_test_total(
            self.shipment_line_item1.product.retail_price,
            self.shipment_line_item1.quantity
        )

        total_retail_test = round(
            self.shipment_line_item1.calculate_retailprice_total(), 2)
        
        self.assertEqual(total_retail_control, total_retail_test)

    def test_shipment_line_items_added(self):
        """
        Confirm that the line items are added to the to the shipment
        object.
        """
        self.assertEqual(len(self.test_shipment.line_items.all()), 2) 
    
    def test_product_inventory_count_deducted(self):
        """
        Confirm that the Product object's inventory count is deducted
        by the quantity specified in the creation of a ShipmentLineItem object.

        Original Inventory Count of self.test_product1 object = 50
        Quantity of self.test_product1 added to ShipLineItem = 10

        50 - 10 = 40
        """
        test_product1 = Product.objects.get(pk=self.test_product1.pk)
        test_product2 = Product.objects.get(pk=self.test_product2.pk)
        self.assertEqual(test_product1.inventory_count, 40)
        self.assertEqual(test_product2.inventory_count, 40)
