from django import forms


class CartAddProductForm(forms.Form):
    """
    Form to add a product to the cart or update its quantity.
    """
    
    quantity = forms.IntegerField(min_value=1, max_value=100, initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)