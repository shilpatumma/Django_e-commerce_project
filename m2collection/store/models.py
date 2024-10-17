from django.db import models
from django.urls import reverse



class Category(models.Model):
    """
    Represents a product category (e.g., Shirts, Pants).
    """
    
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories' # Corrects the plural name in admin
        
    def __str__(self):
        return self.name
    
    
    
class Product(models.Model):
    """
    Represents a product in the store.
    """
    
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True) # Automatically set on creation
    updated = models.DateTimeField(auto_now=True) # Automatically updated on save
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),  # Replace index_together with indexes
        ]
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """
        Returns the URL to access a particular product instance.
        """
        return reverse('store:product_detail', args=[self.id, self.slug])
