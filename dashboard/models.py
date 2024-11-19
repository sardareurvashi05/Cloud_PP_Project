from pyexpat import model
from sre_constants import CATEGORY
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

CATEGORY = [('Electronics', 'Electronics'), ('Furniture', 'Furniture'), ('Clothing', 'Clothing')]

# Create your models here.
class Product(models.Model):
    name= models.CharField(max_length=100,null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)
    quantity_in_stock = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Discount percentage
    reorder_threshold = models.PositiveIntegerField(default=10)  # Reorder threshold
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural ='Product'

    def __str__(self):
        return f'{self.name} - {self.quantity_in_stock}'

    @property
    def stock_value(self):
        """Calculate and return the total stock value."""
        return self.price * self.quantity_in_stock

    @property
    def discounted_price(self):
        """Calculate and return the discounted price."""
        return self.price - (self.price * (self.discount / 100))

    @property
    def reorder_status(self):
        """Check if reorder is needed based on quantity and threshold."""
        return 'Reorder Needed' if self.quantity_in_stock < self.reorder_threshold else 'Stock Sufficient'

class Order(models.Model):
    product =models.ForeignKey(Product, on_delete=models.CASCADE ,null=True)
    staff=models.ForeignKey(User, models.CASCADE ,null=True)
    order_quantity= models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural ='Order'

    def __str__(self):
        return f'{self.product} ordered by {self.staff.username}'
    