from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib import messages
from .forms import UserProfileForm
from .models import UserProfile

class home_view(TemplateView):
    template_name = 'home.html'

def user_login(request):
    if request.method == 'POST':
        # Get the username and password from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Django's built-in authentication function
        user = authenticate(request, username=username, password=password)
        # If new user
        if user:
            # Check user account is active
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to task_add page.
                return redirect('create_profile')
            else:
                # If account is inactive
                messages.error(request, 'Your account is not active.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid login details supplied.')
            return redirect('login')
    else:
        #Nothing has been provided for username or password.
        return render(request, 'login.html', {})

@login_required
def result(request):
    return render(request,'todolist_app/result.html')

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/userauth_app/login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to task_addpage.
    return render(request, 'home.html')

def user_register(request):
    if request.method == 'POST':
        username    = request.POST.get('username')
        email       = request.POST.get('email')
        password1   = request.POST.get('password1')

        form = RegistrationForm(request.POST)
        if form.is_valid():
            my_user = User.objects.create_user(username=username, email=email, password=password1)
            my_user.save()
            # Add a success message
            messages.success(request, 'Registration successful! Please login and complete your profile.')
            return redirect('login')
    else:
        # Clear the form errors to prevent them from being displayed on the page
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def my_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        context = {
            'user': user_profile
        }
        return render(request, 'user_profile.html', context)
    except UserProfile.DoesNotExist:
        messages.warning(request, 'User profile does not exist.')
        return redirect('home')  # Redirect to a relevant page

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user  # Assign the current user to the user_profile
            user_profile.save()
            return redirect('myprofile')  # Redirect to a relevant page after successful profile creation
    else:
        form = UserProfileForm()

    context = {
        'form': form
    }
    return render(request, 'create_profile.html', context)
