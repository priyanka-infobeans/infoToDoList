from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=150)
    email           = models.EmailField()
    profile_photo   = models.ImageField(upload_to='profile_photos', blank=True)
    bio             = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label   = 'todolist_app'
