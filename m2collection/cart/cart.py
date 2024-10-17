from decimal import Decimal
from django.conf import settings
from store.models import Product


# class Cart:
#     """
#         A class to manage the shopping cart stored in the user's
#     session.
#     """


#     def __init__(self, request):
#         """
#         Initialize the cart.
#         """
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#         if not cart:
#         # Save an empty cart in the session
#             cart = self.session[settings.CART_SESSION_ID] = {}
#         self.cart = cart
    
    
#     def add(self, product, quantity=1, update_quantity=False):
#         """
#         Add a product to the cart or update its quantity.
#         """
#         product_id = str(product.id)
#         if product_id not in self.cart:
#             self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
#         if update_quantity:
#             self.cart[product_id]['quantity'] = quantity
#         else:
#             self.cart[product_id]['quantity'] += quantity
#         self.save()
        
        
#     def save(self):
#         """
#         Mark the session as "modified" to ensure it is saved.
#         """
#         self.session.modified = True
        
        
#     def remove(self, product):
#         """
#         Remove a product from the cart.
#         """
#         product_id = str(product.id)
#         if product_id in self.cart:
#             del self.cart[product_id]
#         self.save()
        
        
#     def __iter__(self):
#         """
#         Iterate over the items in the cart and get the products from
#         the database.
#         """
#         product_ids = self.cart.keys()
#         # Get the product objects and add them to the cart
#         products = Product.objects.filter(id__in=product_ids)
#         for product in products:
#             self.cart[str(product.id)]['product'] = product
#         for item in self.cart.values():
#             item['price'] = Decimal(item['price'])
#         item['total_price'] = item['price'] * item['quantity']
#         yield item
        
        
#     def __len__(self):
#         """
#         Count all items in the cart.
#         """
#         return sum(item['quantity'] for item in self.cart.values())
    
    
#     def get_total_price(self):
#         """
#         Calculate the total price of the cart.
#         """
#         return sum(Decimal(item['price']) * item['quantity'] for
#         item in self.cart.values())
        
        
#     def clear(self):
#         """
#         Remove cart from session.
#         """
#         del self.session[settings.CART_SESSION_ID]
#         self.save()



class Cart:
    def __init__(self, request):
        # This might be a session-based cart, for example
        self.cart = request.session.get('cart', {})

    def __iter__(self):
        for item_id, item_data in self.cart.items():
            yield {
                'id': item_id,
                'product': item_data['product'],
                'quantity': item_data['quantity'],
                'price': item_data['price'],
            }

    # def add(self, product, quantity=1):
    #     if product.id in self.cart:
    #         self.cart[product.id]['quantity'] += quantity
    #     else:
    #         self.cart[product.id] = {
    #             'product': product,
    #             'quantity': quantity,
    #             'price': product.price,
    #         }
    #     self.save()

    # def save(self):
    #     self.request.session['cart'] = self.cart

    def add(self, product, quantity=1, update_quantity=False):
            """
            Add a product to the cart or update its quantity.
            """
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            self.save()
            
            
            
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    
    def get_total_price(self):
        """
        Calculate the total price of the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for
        item in self.cart.values())
        
        
    def clear(self):
        """
        Remove cart from session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()