from django import forms
from .models import Order, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity_in_stock', 'discount', 'reorder_threshold']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields= ['product','order_quantity']
