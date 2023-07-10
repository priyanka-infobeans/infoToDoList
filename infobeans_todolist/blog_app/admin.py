from django.contrib import admin
from .models import Blog
from .models import Comment

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_id', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('title', 'content')

admin.site.register(Comment)
