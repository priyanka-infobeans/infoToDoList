from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    user_id     = models.ForeignKey(User, on_delete=models.CASCADE)
    title       = models.CharField(max_length=100)
    content     = models.TextField()
    blog_image  = models.ImageField(upload_to='blog_images/')
    updated_on  = models.DateTimeField(auto_now=True, null=True)
    created_on  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    first_name  = models.CharField(max_length=255)
    email       = models.EmailField()
    subject     = models.CharField(max_length=255)
    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)