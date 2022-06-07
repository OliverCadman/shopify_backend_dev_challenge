from django.urls import path
from . import views

urlpatterns = [
    path("", views.AddProduct.as_view(), name="add_product")
]