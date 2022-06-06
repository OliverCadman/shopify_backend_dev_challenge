from django.db import models
from django.utils.translation import gettext_lazy as _
import re

# Create your models here.
class Product(models.Model):
    """
    Define the Product table.

    Attributes:
        - sku (CharField) - Unique identifier to identify and track each product.
        - brand (CharField) - The manufacturer of the product.
        - colour (CharField) - The colour of the paint.
        - paint_type (CharField) - The type of paint:
            Choices are defined in PaintType class, and passed into
            field definition as 'choices' argument.
        - size (CharField) - The size/volume of the paint being sold:
            Choices defined in Size class as integers, from 1 to 5. These translated
            into volumes in millilitres.
        - cost_price (DecimalField) - The cost price of each individual unit.
        - retail_price (DecimalField) - The retail price of each individual unit.
        - inventory_count (IntegerField) - The current amount of units in stock (defaults to 0).
    """

    class Size(models.IntegerChoices):
        EXTRA_SMALL = 1, _("8ml")
        SMALL = 2, _("15ml")
        MEDIUM = 3, _("30ml")
        LARGE = 4, _("50ml")
        EXTRA_LARGE = 5, _("75ml")

    class PaintType(models.TextChoices):
        OIL = "OL", _("Oil")
        ACRYLIC = "AC", _("Acrylic")
        WATERCOLOR = "WC", _("Watercolor")
        GOUACHE = "GC", _("Gouache")
        PASTEL = "PS", _("Pastel")
        ENCAUSTIC = "EC", _("Encaustic")

    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    brand = models.CharField(max_length=254)
    colour = models.CharField(max_length=254)
    paint_type = models.CharField(
        max_length=2,
        choices=PaintType.choices,
    )
    size = models.IntegerField(
        choices=Size.choices,
    )
    cost_price = models.DecimalField(max_digits=6, decimal_places=2)
    retail_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory_count = models.IntegerField(default=0)

    def get_brand_name(self): 
        """
        Create a brand name representation in SKU format.
        
        If more than one word is present in the string, 
        extract the capital letters from each word and use
        to create initials of words in SKU.

        If one word, and larger than 3 characters, take the first
        three characters. Otherwise, take the whole string.

        Convert all characters to uppercase.
        """
        if len(self.brand.split()) > 1:
            brand_initials = re.findall("[A-Z]+", self.brand.title())
            if brand_initials:
                return "".join(brand_initials)
        elif len(self.brand) > 3:
            return self.brand[:3].upper()
        else:
            return self.brand.upper()
    
    def get_sku(self):
        """
        Prepare SKU field.
        """
        return self.get_brand_name()
    
    def save(self, *args, **kwargs):
        """
        Customise save method to populate SKU field.
        """
        if not self.sku:
            self.sku = self.get_sku()
        super().save(*args, **kwargs)
  

    def __str__(self):
        return self.name

