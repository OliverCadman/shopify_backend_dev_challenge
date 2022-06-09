from django.urls import path
from . import views

urlpatterns = [
    path("create_shipment/", views.create_shipment_view, name="create_shipment")
]