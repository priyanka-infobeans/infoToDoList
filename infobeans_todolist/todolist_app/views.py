from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .forms import TodoListForm
from .models import TodoList
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
class index_view(TemplateView):
    template_name = 'base.html'

def task_add(request):
    try:
        todo_list = TodoList.objects.all()
        print(todo_list)
        context = {
            'tasks': todo_list,
        }
        if request.method == 'POST':
            title = request.POST['task_title']
            description = request.POST['task_description']
            status = bool(request.POST.get('task_status', False))

            TodoList.objects.create(task_title=title, task_description=description, task_status=status)
            context = {
                'tasks': todo_list,
                'success_message': 'Task added on listing!',
            }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        context = {
            'tasks': '',
        }

    return render(request, 'todolist_app/task_add.html', context)
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
        return redirect('todolist_app:task_list')
    return render(request, 'todolist_app/confirm_delete.html', {'task': task})

def edit_task(request, task_id):
    task = get_object_or_404(TodoList, pk=task_id)
    if request.method == 'POST':
        form = TodoListForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todolist_app:task_list')
    else:
        form = TodoListForm(instance=task)
    return render(request, 'todolist_app/task_update.html', {'form': form, 'task': task})

def update_title_status(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            task_id     = request.POST.get('task_id')
            is_checked  = request.POST.get('is_checked')

            # Retrieve the ToDoList object based on the task_id
            try:
                print('step1')
                todo = TodoList.objects.get(id=task_id)
                todo.title_status = is_checked
                todo.save()
                return JsonResponse({'success': True})
            except TodoList.DoesNotExist:
                print('step2')
                return JsonResponse({'success': False, 'error': 'Task not found.'})
    else:
        print('step3')
        return JsonResponse({'success': False, 'error': 'Invalid request.'})