from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm


class AddProductView(CreateView):
    model = Product
    form_class = ProductForm
    
    def get_success_url(self):
        return reverse("product_list")

add_product_view = login_required(AddProductView.as_view())


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"

product_list_view = login_required(ProductListView.as_view())

