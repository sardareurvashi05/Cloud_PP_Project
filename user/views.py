from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,UserUpdateForm,ProfileUpdateForm,OrderRequestForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from .s3_utils import upload_to_s3,get_profile_picture
from urllib.parse import unquote,quote
from . import views
from django.shortcuts import render, redirect
from django.contrib import messages

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
