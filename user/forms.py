from django import forms
from .models import Profile
from django.contrib.auth.models import User
from .models import Order
from django.contrib.auth.forms import UserCreationForm

class OrderRequestForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_quantity']

class CreateUserForm(UserCreationForm):
    email=forms.EmailField()

    class Meta:
        model = User
        fields =['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=['address','phone','image']



