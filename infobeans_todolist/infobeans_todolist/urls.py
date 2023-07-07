"""infobeans_todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.task_add, name='task_add')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='task_add')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('', include('blog_app.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from infobeans_todolist import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view.as_view(), name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('create/', views.create_user_profile, name='create_user_profile'),
    path('user_profile/<str:name>/', views.user_profile, name='user_profile'),
    path('todolist_app/', include('todolist_app.urls')),
    path('blog_app/', include('blog_app.urls')),
    path('social_app/', include('social_app.urls')),
]