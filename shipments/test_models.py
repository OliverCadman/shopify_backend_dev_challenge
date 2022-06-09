from django.test import TestCase
from .models import Shipment, ShipmentLineItem
from products.models import Product
from .test_utils import calculate_test_total


class ShipmentModelTest(TestCase):

    def setUp(self):
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


    def test_shipment_line_items_added_and_total_updated(self):

        self.test_shipment.update_total()
        print("TEST SHIPMENT", self.test_shipment.order_total_retail)
        print("TEST SHIPMENT", self.test_shipment.grand_total_retail)
        print("TEST SHIPMENT", self.test_shipment.order_total_cost)

        self.assertEqual(len(self.test_shipment.line_items.all()), 2)

        