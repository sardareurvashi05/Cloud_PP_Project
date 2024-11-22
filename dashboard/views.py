from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Order
from .forms import ProductForm, OrderForm
from libs.product_calculator import calculate_stock_value, calculate_discounted_price, check_reorder_status, generate_inventory_report
import json
import openpyxl
from openpyxl.styles import Font, Alignment
from django.http import HttpResponse
from user.sqs_service import send_message_to_sqs
from user.gateway_utils import sendEmail 

# Helper function to calculate product details
def get_product_details(product):
    stock_value = calculate_stock_value(product.price, product.quantity_in_stock)
    discounted_price = calculate_discounted_price(product.price, product.discount)
    reorder_status = check_reorder_status(product.quantity_in_stock, product.reorder_threshold)
    return stock_value, discounted_price, reorder_status


@login_required
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    products_count = Product.objects.count()  # Correct: Get the count of products
    orders_count = orders.count()  # Get the count of orders
    staff_count = User.objects.count()  # Correct: Use count() instead of .all.count()

    form = OrderForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.staff = request.user
        instance.save()
        product = form.cleaned_data.get('product')
        product_name = product.name  # Access the name attribute of the product
        messages.success(request, f'{product_name} has been added')
        
         # Prepare email data to send to SQS
        email_message = {
            "email": request.user.email,  # Replace with actual recipient email
            "subject": "Order Confirmation",
            "body": f"Your order for {product_name} has been placed successfully.",
        }
        print(email_message)
        # Send email data to SQS
        message_body = json.dumps(email_message)
        response = send_message_to_sqs(message_body)
        print(response)
        status_code = sendEmail()
        print(f"Status code: {status_code} ")
        return redirect('dashboard-index')
    
    context = {
        'orders': orders,
        'form': form,
        'products': products,
        'products_count': products_count,
        'orders_count': orders_count,
        'staff_count': staff_count,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count  = Order.objects.all().count()
    products_count = Product.objects.all().count()
    context={
        'workers': workers,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'products_count':products_count,
        }
    return render(request, 'dashboard/staff.html',context)


@login_required
def staff_detail(request, pk):
    worker = get_object_or_404(User, id=pk)
    return render(request, 'dashboard/staff_details.html', {'worker': worker})


@login_required
def product_delete(request, pk):
    item = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'Product {item.name} has been deleted')
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html', {'item': item})


@login_required
def product_update(request, pk):
    item = get_object_or_404(Product, id=pk)
    form = ProductForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, f'Product {item.name} has been updated')
        return redirect('dashboard-product')
    
    return render(request, 'dashboard/product_update.html', {'form': form})


@login_required
def product(request):
    items = Product.objects.all()
    workers_count = User.objects.all().count()
    orders_count  = Order.objects.all().count()
    products_count = Product.objects.all().count()
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'New product added successfully')
        return redirect('dashboard-product')
    else:
        form=ProductForm()
        context={
            'items': items,
            'form': form,
            'workers_count':workers_count,
            'orders_count':orders_count,
            'products_count':products_count,
            }
    return render(request, 'dashboard/product.html',context)


@login_required
def order(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    workers_count = User.objects.all().count()
    products_count = Product.objects.all().count()
    context={
        'orders': orders,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'products_count':products_count,
        }
    return render(request, 'dashboard/order.html', context)


@login_required
def product_list(request):
    products = Product.objects.all()
    inventory_report = generate_inventory_report(products)
    return render(request, 'dashboard/product_list.html', {
        'products': products,
        'inventory_report': inventory_report
    })


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    stock_value, discounted_price, reorder_status = get_product_details(product)
    
    context = {
        'product': product,
        'stock_value': stock_value,
        'discounted_price': discounted_price,
        'reorder_status': 'Reorder Needed' if reorder_status else 'Stock Sufficient',
    }
    return render(request, 'product/product_detail.html', context)


@login_required
def recalculate_stock(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        data = json.loads(request.body)
        price = data.get('price', product.price)
        quantity_in_stock = data.get('quantity_in_stock', product.quantity_in_stock)
        
        stock_value = calculate_stock_value(price, quantity_in_stock)
        return JsonResponse({'stock_value': stock_value})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def export_to_excel(request):
    # Create a new workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Product List"

    # Define the header
    headers = ["Product Name", "Stock Value", "Discounted Price", "Reorder Status"]
    ws.append(headers)

    # Style the header
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    # Retrieve data and add rows to the worksheet
    for report in Product.objects.all():  # Replace with your queryset
        reorder_status = "Reorder Needed" if report.reorder_status == 'Reorder Needed' else "In Stock"
        ws.append([report.name, report.stock_value, report.discounted_price, reorder_status])

    # Set response headers to make it downloadable
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="Product_List.xlsx"'

    # Save the workbook to the response
    wb.save(response)
    return response