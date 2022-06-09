from django.urls import path
from . import views

urlpatterns = [
    path("", views.add_product_view, name="add_product"),
    path("product_list/", views.product_list_view, name="product_list"),
    path("edit_product/<int:pk>", views.product_edit_view, name="edit_product")
]