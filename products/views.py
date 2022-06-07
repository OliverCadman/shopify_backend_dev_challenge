from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .models import Product


class AddProduct(CreateView):
    model = Product
    fields = [
        'name',
        'brand',
        'size',
        'colour',
        'paint_type',
        'cost_price',
        'retail_price'
    ]

