from django.db import models
from django.utils.translation import gettext_lazy as _

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

    sku = models.CharField(max_length=254)
    brand = models.CharField(max_length=254)
    colour = models.CharField(max_length=254)
    paint_type = models.CharField(
        max_length=2,
        choices=PaintType.choices,
    )
    size = models.CharField(
        max_length=2,
        choices=Size.choices,
    )
    cost_price = models.DecimalField(max_digits=6, decimal_places=2)
    retail_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory_count = models.IntegerField(default=0)

