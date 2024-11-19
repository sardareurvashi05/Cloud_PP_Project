from django.urls import path
from . import views

urlpatterns = [
    path('staff_index/', views.make_request, name='staff_index'),
    # Other URL patterns
]
