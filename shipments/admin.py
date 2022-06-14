from django.contrib import admin
from .models import Shipment, ShipmentLineItem


# Register your models here.
admin.site.register(Shipment)
admin.site.register(ShipmentLineItem)