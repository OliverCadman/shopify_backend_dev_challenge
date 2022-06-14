from django.db import models
from django.utils.translation import gettext_lazy as _
import re


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


    def get_brand_name_repr(self): 
        """
        Return an SKU representation of the product's brand name.
        """
        return initialize_string(self.brand)
    
    def get_color_repr(self):
        """
        Return an SKU representation of the product's colour.
        """
        return initialize_string(self.colour)
    
    def get_size_repr(self):
        """
        Return an SKU repesentation of the product's size.
        """
        return self.size
    
    def get_paint_type_repr(self):
        """
        Return an SKU representation of the product's paint type.
        """
        return self.paint_type

    def get_sku(self):
        """
        Prepare full SKU field.
        """
        brand_name = self.get_brand_name_repr()

        paint_type = self.get_paint_type_repr()

        color = self.get_color_repr()

        size = self.get_size_repr()

        return f"{brand_name}-{color}-{paint_type}-{size}"
    
    def decrement_inventory_count(self, quantity):
        print("DECREMENTING INVENTORY COUNT...")
        if self.inventory_count > 0 or self.inventory_count > quantity:
            self.inventory_count -= quantity
            self.save()
        else:
            return None

    def save(self, *args, **kwargs):
        """
        Customise save method to populate SKU field.
        """
        if not self.sku:
            self.sku = self.get_sku()
        super().save(*args, **kwargs)
  

    def __str__(self):
        """
        Return string representation of product object.
        """
        return self.name



def initialize_string(string):
    """
    Create a field string representations in SKU format.
        
        If more than one word is present in the string, 
        extract the capital letters from each word and use
        to create initials of words in SKU.

        If one word, and larger than 3 characters, take the first
        three characters. Otherwise, take the whole string.

        Convert all characters to uppercase.
    """
    if len(string.split()) > 1:
        multiple_words = re.findall("[A-Z]+", string.title())
        if multiple_words:
            return "".join(multiple_words)
    elif len(string) > 3:
        return string[:3].upper()
    else:
        return string.upper()
    


