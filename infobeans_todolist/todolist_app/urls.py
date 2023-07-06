from django.urls import path
from todolist_app import views

app_name = 'todolist_app'

urlpatterns=[
    path('task_list/', views.task_list, name='task_list'),
    path('task_add/', views.task_add, name='task_add'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
]