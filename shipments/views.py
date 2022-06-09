from django.shortcuts import render
from django.views.generic import CreateView
from .models import Shipment


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

create_shipment_view = CreateShipmentView.as_view()