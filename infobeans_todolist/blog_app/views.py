from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views import generic
from django.shortcuts import render, redirect
from .forms import BlogForm
from django.contrib.auth.models import User
from .models import Blog,Comment
from .forms import CommentForm
def index_view(request):
    blogs = Blog.objects.all()

    context = {
        'blogs': blogs,
    }

    return render(request, 'blog_app/index.html', context)
class about_view(TemplateView):
    template_name = 'blog_app/about.html'

class blog_view(TemplateView):
    template_name = 'blog_app/blog.html'

class contact_view(TemplateView):
    template_name = 'blog_app/contact.html'
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            user_id = request.user.id
            user = User.objects.get(id=user_id)

            # user = User.objects.get(id=user_id)
            blog.user_id = user
            blog.save()
            return redirect('blog_app:blog_detail', pk=blog.pk)  # Redirect to the blog detail page
    else:
        form = BlogForm()

    return render(request, 'blog_app/create_blog.html', {'form': form})
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    comments = Comment.objects.filter(blog=blog)  # Fetch comments related to the blog
    comment_count = comments.count()  # Get the comment count
    related_posts = Blog.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog  # Assign the blog_id to the comment
            comment.user = request.user  # Assign the current user to the comment
            comment.save()
            return redirect('blog_app:blog_detail', pk=pk)
    else:
        form = CommentForm()

    context = {
        'blog': blog,
        'comments': comments,
        'form': form,
        'comment_count': comment_count,
        'related_posts':related_posts,
    }
    return render(request, 'blog_app/blog_detail.html', context)

class post_list(TemplateView):
    template_name = 'blog_app/home.html'

def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_app:blog_detail', pk=pk)
    else:
        form = BlogForm(instance=blog)

    context = {
        'form': form,
    }
    return render(request, 'blog_app/blog_update.html', context)

def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    print(pk)
    blog.delete()
    return redirect('blog_app:index')
