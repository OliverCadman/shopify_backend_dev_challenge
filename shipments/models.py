from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_countries.fields import CountryField
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from products.models import Product
import uuid



class Shipment(TimeStampedModel):

    """
    Represents a Shipment Object.

    Attributes:
        
        - shipment_number (CharField) - a UUID identifier for the shipment

        - recipient_name (CharField) - The name of the recipient of the shipment.

        - email (EmailField) - The email address of the recipient.

        - phone (IntegerField) - The recipient's phone number.

        - building_name (CharField) (Optional) - The name of shipping destination.

        - street_address1 (CharField) - The first line of recipient's address.

        - street_address2 (CharField) (Optional) - The second line of recipient's address.

        - town_or_city (CharField) - The town/city of shipping destination.

        - county (CharField) (Optional) - The county of the shipping destination.

        - country (CountryField) - The country of the shipping destination.

        - postcode (Charfield) - The postcode of the shipping destination.

        - delivery_cost (DecimalField) - The shipping cost.

        - order_retail_total (DecimalField) - The total of the order.

        - grand_retail_total (DecimalField) - The total of the order with shipping costs.

        - order_cost_total (DecimalField) - The total cost price of the order.

        status (int) - The current status of the shipment:
            1 - Received
            2 - Processing
            3 - Fulfilled
            4 - Cancelled
    """


    class Status(models.IntegerChoices):
        RECEIVED = 1, _("Received")
        PROCESSING = 2, _("Processing")
        FULFILLED = 3, _("Fulfilled")
        CANCELLED = 4, _("Cancelled")


    shipment_number = models.CharField(max_length=32, editable=False)
    recipient_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label="Country *", null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total_retail = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total_retail = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    order_total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    status = models.IntegerField(choices=Status.choices)

    def generate_shipment_number(self):
        """
        Generate a random, unique shipment number using UUID.
        """
        return uuid.uuid4().hex.upper()
    
    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """

        self.order_total_cost = self.line_items.aggregate(
            Sum("costprice_total")
        )["costprice_total__sum"] or 0

        self.order_total_cost = round(self.order_total_cost, 2)
        
        self.order_total_retail = self.line_items.aggregate(
            Sum("retailprice_total")
        )["retailprice_total__sum"] or 0

        self.order_total_retail = round(self.order_total_retail, 2)

        self.delivery_cost = (
            self.order_total_retail * settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        
        self.grand_total_retail = self.order_total_retail + self.delivery_cost

        self.grand_total_retail = round(self.grand_total_retail, 2)
        self.save()


    def save(self, *args, **kwargs):
        """
        Override default save method to set
        the shipment number, if it hasn't been set 
        already.
        """

        if not self.shipment_number:
            self.shipment_number = self.generate_shipment_number()
        super().save(*args, **kwargs)



class ShipmentLineItem(models.Model):
    """
    Represents an individual item of a given shipment.

    Attributes:

        - shipment (ForeignKey) - A many-to-one field to a given shipment object.

        - product (ForeignKey) - A many-to-one field to a given product object.

        - quantity (IntegerField) - The quantity of a single type of product.

        - costprice_total (DecimalField) - The total of the cost price
        for a given product type:
            (product.cost_price * quantity)

        - retailprice_total (DecimalField) - The total of the retail price
        for a given product type:
            (product.retail_price * quantity)
    """


    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="in_shipping")
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="line_items")
    quantity = models.IntegerField(default=0)
    costprice_total = models.DecimalField(max_digits=6, decimal_places=2)
    retailprice_total = models.DecimalField(max_digits=6, decimal_places=2)

    def calculate_costprice_total(self):
        """
        Calculate the total cost price of the line item.
        """
        return self.product.cost_price * self.quantity
    
    def calculate_retailprice_total(self):
        """
        Calculate the total retail price of the line item.
        """
        return self.product.retail_price * self.quantity
    
    def save(self, *args, **kwargs):
        """
        Override default save method to set the
        costprice_total and retailprice_total fields.
        """

        self.costprice_total = self.calculate_costprice_total()
        self.retailprice_total = self.calculate_retailprice_total()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"SKU {self.product.sku} on order {self.shipment.shipment_number}"
