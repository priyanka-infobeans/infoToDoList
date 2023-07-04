from django.urls import path
from todolist_app import views

app_name = 'todolist_app'

urlpatterns=[
    path('', views.user_login, name='user_login'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task_add/', views.task_add, name='task_add'),
    path('create_task/', views.create_task, name='create_task'),
    path('task_list', views.task_list, name='task_list'),

]