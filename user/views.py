from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,UserUpdateForm,ProfileUpdateForm,OrderRequestForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from .s3_utils import upload_to_s3,get_profile_picture
from urllib.parse import unquote,quote
from .sns_utils import publish_to_sns
from . import views
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderRequestForm
from user.sns_utils import publish_to_sns, subscribe_email_to_topic, check_if_subscribed

def make_request(request):
    if request.method == 'POST':
        form = OrderRequestForm(request.POST)
        if form.is_valid():
            try:
                # Create order and associate it with the logged-in user
                order = form.save(commit=False)
                order.staff = request.user
                order.save()  # Save the order and assign an ID
                
                # Create the SNS message
                message = (
                    f"New order request from {request.user.username}.\n"
                    f"Product: {order.product.name},\n"
                    f"Quantity: {order.order_quantity},\n"
                    f"Order ID: {order.id}"
                )
                subject = "New Order Request"
                
                # Publish to SNS
                topic_arn = 'arn:aws:sns:us-east-1:763605845924:my-inventory-reports-topic'
                
                admin_email = 'admin@gmail.com'
                subscribe_email_to_topic(topic_arn, admin_email)
                if not check_if_subscribed(topic_arn, admin_email):
                    subscribe_email_to_topic(topic_arn, admin_email)
                else:
                    print("Email is already subscribed.")
                publish_to_sns(topic_arn, message, subject)

                # Success message and redirect
                messages.success(request, "Order request submitted successfully and notification sent.")
                return redirect('success_page')  # Replace 'success_page' with your success view name
            except Exception as e:
                # Log the error and show an error message
                print(f"Error sending SNS notification: {e}")
                messages.error(request, "Order request submitted but failed to send notification.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = OrderRequestForm()

    return render(request, 'user/staff_index.html', {'form': form})

# Create your views here.
def register(request):
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
    else:
        form=CreateUserForm()
    context={
        'form':form
        }
    return render(request, 'user/register.html', context)
    
@login_required
def profile(request):
    return render(request, 'user/profile.html')
    
@login_required
def profile_update(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(staff=request.user)  # Create profile if missing

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user and profile forms
            user_form.save()
            profile = profile_form.save(commit=False)
            # Check if an image file is uploaded
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                username = request.user.username
                s3_url = upload_to_s3(image_file, username)
                #print(s3_url)
                if s3_url:
                    profile.image = s3_url
                else:
                    print("Failed to upload the image to S3.")
            
            profile.save()
            image_url = get_profile_picture(f"{username}.jpg")
            context = {
                    'image_url': image_url,  # Pass the image URL to the template
            }
            return render(request, 'user/profile.html', context)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile_update.html', context)
