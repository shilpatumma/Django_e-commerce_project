from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .cart import Cart
from django.urls import reverse
from .forms import CartAddProductForm


def cart_detail(request):
    """
    Displays the cart details and allows modifications.
    """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_add(request, product_id):
    """
    Adds a product to the cart or updates its quantity.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
    cart.add(
        product=product,
        quantity=cd['quantity'],
        update_quantity=cd['update']
    )
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    """
    Removes a product from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    cart.remove(product)
    return redirect('cart:cart_detail')