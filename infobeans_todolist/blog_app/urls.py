from . import views
from django.urls import path

app_name = 'blog_app'

urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('home/', views.post_list.as_view(), name='home'),
    path('about/', views.about_view.as_view(), name='about'),
    path('blog/', views.blog_view.as_view(), name='blog'),
    path('contact/', views.contact_view.as_view(), name='contact'),
    path('create/', views.create_blog, name='create'),
    path('blog_detail/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog_update/<int:pk>/', views.blog_update, name='blog_update'),
    path('blog_delete/<int:pk>', views.blog_delete, name='blog_delete'),
]
