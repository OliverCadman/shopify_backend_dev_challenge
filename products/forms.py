from .models import Product
from django import forms


class ProductForm(forms.ModelForm):
    """
    Customise UI of Product Form.
    """
    class Meta:
        model = Product
        exclude = ("sku",)
    

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and initial values for specific fields
        of ProductForm.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            "name": "Professional Water Colour Tubes",
            "brand": "Winsor & Newton",
            "colour": "Cadmium Orange",
            "cost_price": "4.99",
            "retail_price": "19.99"
        }

        self.initial["paint_type"] = "OL"
        self.initial["size"] = 1

        for field in self.fields:
            if field != "paint_type" and field != "size" and field != "inventory_count":
                placeholder = f"{placeholders[field]}"
                self.fields[field].widget.attrs["placeholder"] = placeholder

        