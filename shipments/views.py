from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.forms import modelformset_factory
from .models import Shipment
from products.models import Product


class CreateShipmentView(CreateView):
    template_name = "shipments/shipment_form.html"
    model = Shipment
    fields = [
        "recipient_name",
        "email",
        "phone_number",
        "street_address1",
        "street_address2",
        "town_or_city",
        "county",
        "country",
        "postcode"
    ]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_products = Product.objects.all()
        context["products"] = all_products
        return context
    
    def post(self, *args, **kwargs):
        print("POST", self.request)
        return super().post(*args, **kwargs)
    

create_shipment_view = CreateShipmentView.as_view()
