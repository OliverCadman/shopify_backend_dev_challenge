from enum import unique
from itertools import product
from operator import add
import re
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib import messages
from .models import Shipment, ShipmentLineItem
from .forms import ShipmentForm
from products.models import Product


def create_shipment(request):

    if request.method == "POST":
        bag = request.session.get("bag", {})
        shipment_form = ShipmentForm(request.POST or None)

        if shipment_form.is_valid():
            shipment = shipment_form.save(commit=False)
            shipment.status = 1
            shipment.save()
            print("SHIPMENT", shipment)
            for item_id, item_data in bag.items():
                print("ITEM ID:", item_id, type(item_id), "ITEM DATA:", item_data)
                try:
                    product = Product.objects.get(
                        pk=int(item_id)
                    )

                    order_line_item = ShipmentLineItem(
                        product=product,
                        shipment=shipment,
                        quantity=item_data
                    )
                    order_line_item.save()
                    
                    product.decrement_inventory_count(item_data)
                    shipment.update_total()
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "Product not found in database."
                    )
                    shipment.delete()
                    return redirect(reverse("create_shipment"))
            del request.session["bag"]
            messages.success(request, "Shipment placed.")
            return redirect(reverse("create_shipment"))
        else:
            print("ERRORS", shipment_form.errors)
    else:
        shipment_form = ShipmentForm()
        bag = request.session.get("bag", {})
    
    all_products = Product.objects.all()
    bag_items = []
        
    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        bag_items.append({
            "item_id": item_id,
            "quantity": item_data,
            "product": product
        })

    template = "shipments/shipment_form.html"
    context = {
        "form": shipment_form,
        "products": all_products,
        "added_products": bag_items,
    }


    return render(request, template, context)


def add_to_shipment(request, product_id):

    del request.session["bag"]

    current_product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get(f"quantity_{product_id}"))

    if int(quantity) > current_product.inventory_count:
        messages.error(
            request, f"Not enough products in inventory.")
        
        return redirect(reverse("create_shipment"))
    
    bag = request.session.get("bag", {})

    if str(product_id) in list(bag.keys()):
        bag[str(product_id)] += quantity
        messages.success(
            request, f"{quantity} units of {current_product.name} added to shipment")
    else:
        bag[product_id] = quantity
        messages.success(
            request, f"{quantity} units of {current_product.name} added to shipment")
    
    request.session["bag"] = bag
    
    return redirect(reverse("create_shipment"))

def nested_dict_pairs_iterator(dict_obj):
    ''' This function accepts a nested dictionary as argument
        and iterate over all values of nested dictionaries
    '''
    # Iterate over all key-value pairs of dict argument
    for key, value in dict_obj.items():
        # Check if value is of dict type
        if isinstance(value, dict):
            # If value is dict then iterate over all its values
            for pair in  nested_dict_pairs_iterator(value):
                yield (key, *pair)
        else:
            # If value is not dict type then yield the value
            yield (key, value)

def check_if_duplicate_id(list_of_elems):
    for elem in list_of_elems:
        if list_of_elems.count(elem) > 1:
            return set(list_of_elems)
        return False