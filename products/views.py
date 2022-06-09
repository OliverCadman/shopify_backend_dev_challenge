from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm


class AddProductView(CreateView):
    """
    Add a new product to the inventory.
    """
    model = Product
    form_class = ProductForm
    
    def get_success_url(self):
        """
        Redirect to Product List upon successful form submission.
        """
        return reverse("product_list")

add_product_view = login_required(AddProductView.as_view())


class ProductListView(ListView):
    """
    Display the complete list of products in the inventory.
    """
    model = Product
    template_name = "products/product_list.html"

    paginate_by = 10

product_list_view = login_required(ProductListView.as_view())


class EditProductView(UpdateView):
    model = Product
    form_class = ProductForm

    template_name_suffix = "_update_form"


    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print("context", context)
        return context
    
    def get_success_url(self):
        """
        Redirect to Product List upon successful form submission.
        """
        return reverse("product_list")


product_edit_view = login_required(EditProductView.as_view())


