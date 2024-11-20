from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    image = models.ImageField(default='avatar.jpg', upload_to='Profile_Images',max_length=2000)

    objects = models.Manager()

    def __str__(self):
        return f'{self.staff} Profile'

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')

    def __str__(self):
        # The order has an id after being saved to the database.
        return f"Order {self.pk} - {self.product.name}" if self.pk else f"Order (unsaved) - {self.product.name}"
