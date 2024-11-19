from itertools import product
from django.urls import path
from .import views
from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='dashboard-index'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('staff/detail/<int:pk>/', views.staff_detail, name='dashboard-staff-detail'),
    path('product/', views.product, name='dashboard-product'),
    path('product/delete/<int:pk>/', views.product_delete, name='dashboard-product-delete'),
    path('product/list/', views.product_list, name='dashboard-product-list'),
    path('product/update/<int:pk>/', views.product_update, name='dashboard-product-update'),
    path('order/', views.order, name='dashboard-order'),
    path('export-excel/', views.export_to_excel, name='export_to_excel'),
    path('recalculate_stock/<int:product_id>/', views.recalculate_stock, name='recalculate_stock'),
    ]




