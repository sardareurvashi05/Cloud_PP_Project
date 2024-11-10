from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,UserUpdateForm,ProfileUpdateForm
from .models import Profile
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
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
            user_form.save()
            profile_form.save()
            return redirect('user-profile')  # Redirect to the profile page after updating
  # Redirect to the profile page after updating
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile_update.html', context)

