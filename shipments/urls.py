from django.urls import path
from . import views

urlpatterns = [
    path("create_shipment/", views.create_shipment, name="create_shipment"),
    path("add_to_shipment/<int:product_id>", views.add_to_shipment, name="add_to_shipment")
]