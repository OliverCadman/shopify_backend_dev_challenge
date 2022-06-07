from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .models import Product
from .forms import ProductForm


class AddProduct(CreateView):
    model = Product
    form_class = ProductForm
    

