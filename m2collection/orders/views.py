from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from .forms import OrderCreateForm
from django.conf import settings
import stripe
from django.urls import reverse
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY # Initialize Stripe with secret key


@login_required
def order_create(request):
    """
    Handles the creation of an order and processes payment via
    Stripe.
    """
    
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Your cart is empty.")
    return redirect('store:product_list')


    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Create Order object but don't save to database yet
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            # Create OrderItem objects for each item in the cart
            for item in cart:
                OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
                )
                
                # Process payment with Stripe

            try:
                charge = stripe.Charge.create(amount=int(cart.get_total_price() * 100), # Amount in cents
                currency='usd',
                description=f'Order {order.id}',
                source=request.POST['stripeToken']
                )
                # Save the charge ID in the order
                order.paid = True
                order.stripe_charge_id = charge.id
                order.save()
                # Clear the cart
                cart.clear()
                messages.success(request, "Your order has been placed successfully.")
                return redirect('orders:order_detail', order_id=order.id)
            
            except stripe.error.CardError as e:
                messages.error(request, "Your card was declined.")
                
                
    else:
        form = OrderCreateForm()

    context = {
        'cart': cart,
        'form': form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'orders/order/create.html', context)


@login_required
def order_detail(request, order_id):
    """
    Displays the details of a specific order.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order/detail.html', {'order': order})
