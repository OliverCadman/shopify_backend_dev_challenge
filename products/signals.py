
from django.dispatch import receiver
from django.db.models.signals import post_save
from shipments.models import ShipmentLineItem
from products.models import Product



@receiver(post_save, sender=ShipmentLineItem)
def update_product_quantity(sender, instance, created, **kwargs):
    """
    Update inventory count of Product object when ShipmentLineItem
    is created.
    """

    if created:
        line_item = instance
        product_id = instance.pk

        # Retrieve the quantity of items in the ShipmentLineItem
        product_quantity = instance.quantity
        current_product = Product.objects.get(pk=product_id)

        # Deduct ShipmentLineItem quantity from Product's inventory count
        # and update the inventory_count field in Product object.
        current_product.inventory_count -= product_quantity
        current_product.save()

        line_item.shipment.update_total()

        