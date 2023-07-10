from django import forms
from .models import Blog
from .models import Comment

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'blog_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control mb-4'})
        self.fields['content'].widget.attrs.update({'class':'form-control mb-4'})
        self.fields['blog_image'].widget.attrs.update({'class': 'mb-5'})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['first_name', 'email', 'subject', 'content']