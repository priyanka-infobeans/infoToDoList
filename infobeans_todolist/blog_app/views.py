from django.views import generic
from .models import Post
from django.views.generic import TemplateView
from .forms import PostForm

class index_view(TemplateView):
    template_name = 'blog_app/index.html'

class about_view(TemplateView):
    template_name = 'blog_app/about.html'

class blog_view(TemplateView):
    template_name = 'blog_app/blog.html'

class contact_view(TemplateView):
    template_name = 'blog_app/contact.html'
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog_app/index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog_app/post_detail.html'

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Redirect to post list view after successful creation
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})