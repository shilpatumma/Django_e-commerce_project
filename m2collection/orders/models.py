from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.utils import timezone


class Order(models.Model):
    """
    Represents a customer's order.
    """
        
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False) # Indicates if the order has been paid
    stripe_charge_id = models.CharField(max_length=255, blank=True) # Stores Stripe charge ID
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        """
        Calculates the total cost of the order by summing the cost
        of each item.
        """
        return sum(item.get_cost() for item in self.items.all())


    
class OrderItem(models.Model):
    """
    Represents an individual item within an order.
    """
    
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at the time of order
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.id}'
    
    def get_cost(self):
        """
        Calculates the cost of the item based on price and quantity.
        """
        return self.price * self.quantity
    
    
    
    