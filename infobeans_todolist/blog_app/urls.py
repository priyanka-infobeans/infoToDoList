from . import views
from django.urls import path
from .views import create_post

app_name = 'blog_app'

urlpatterns = [
    path('index/', views.index_view.as_view(), name='index'),
    path('home/', views.PostList.as_view(), name='home'),
    path('about/', views.about_view.as_view(), name='about'),
    path('blog/', views.blog_view.as_view(), name='blog'),
    path('contact/', views.contact_view.as_view(), name='contact'),
    path('post/create/', views.create_post, name='create_post'),
    path('post_details/', views.PostDetail.as_view(), name='post_details'),
]