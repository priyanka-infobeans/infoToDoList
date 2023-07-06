from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib import messages
from .forms import UserProfileForm

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
                return redirect('login')
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
            messages.success(request, 'Registration successful!')
            return redirect('create_user_profile')
    else:
        # Clear the form errors to prevent them from being displayed on the page
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def user_profile(request):
    user = request.user
    user_profile = user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {'form': form}
    return render(request, 'user_profile.html', context)

def create_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile created successful!')
            return redirect('user_profile')
    else:
        form = UserProfileForm()
    return render(request, 'create_user_profile.html', {'form': form})