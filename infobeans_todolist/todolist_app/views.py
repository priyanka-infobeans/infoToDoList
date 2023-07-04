from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .forms import TodoListForm
from .models import TodoList

# Create your views here.
class index_view(TemplateView):
    template_name = 'todolist_app/base.html'

def create_task(request):
    if request.method == 'POST':
        title       = request.POST['task_title']
        description = request.POST['task_description']
        status      = bool(request.POST.get('task_status', False))

        TodoList.objects.create(task_title=title, task_description=description, task_status=status)
        context = {
            'success_message': 'Task added on listing!',
        }
        return render(request, 'todolist_app/task_add.html', context=context)

def task_add(request):
    try:
        TodoList = TodoList.objects.all()
        print(TodoList)
        context = {
            'todoList': TodoList,
        }
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        context = {
            'todoList': '',
        }

    return render(request, 'todolist_app/task_add.html', context)
def user_login(request):
    if request.method == 'POST':
        # Get the username and password from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Django's built-in authentication function
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        print('step1')
        # If new user
        if user:
            print('step2')
            # Check user account is active
            if user.is_active:
                print('step3')
                # Log the user in.
                login(request, user)
                # Send the user back to task_add page.
                return redirect('task_list')
            else:
                print('step4')
                # If account is inactive
                return HttpResponse("Your account is not active.")
        else:
            print('step5')
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        #Nothing has been provided for username or password.
        return render(request, 'todolist_app/login.html', {})

@login_required
def result(request):
    return render(request,'todolist_app/result.html')

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/userauth_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to task_addpage.
    return render(request, 'todolist_app/login.html')

def user_register(request):
    if request.method == 'POST':
        username    = request.POST.get('username')
        email       = request.POST.get('email')
        password1   = request.POST.get('password1')

        form = RegistrationForm(request.POST)
        if form.is_valid():
            my_user = User.objects.create_user(username=username, email=email, password=password1)
            my_user.save()
            return render(request, 'todolist_app/login.html', {})
    else:
        # Clear the form errors to prevent them from being displayed on the page
        form = RegistrationForm()
    return render(request, 'todolist_app/register.html', {'form': form})

def task_list(request):
    try:
        tasks = TodoList.objects.all()
        print(tasks)
    except Exception as e:
        print(f"Error occurred: {str(e)}")

    context = {
        'tasks': tasks,
    }
    return render(request, 'todolist_app/task_list.html', context)

def delete_task(request, task_id):
    task = get_object_or_404(TodoList, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('todolist_app/task_list')
    return render(request, 'todolist_app/confirm_delete.html', {'task': task})

def edit_task(request, task_id):
    task = get_object_or_404(TodoList, pk=task_id)
    if request.method == 'POST':
        form = TodoListForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todolist_app/task_list')
    else:
        form = TodoListForm(instance=task)
    return render(request, 'todolist_app/task_update.html', {'form': form, 'task': task})
