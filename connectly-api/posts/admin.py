from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at')
    search_fields = ('username', 'email')
    ordering = ('created_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'created_at')
    search_fields = ('content',)
    list_filter = ('author', 'created_at')
    ordering = ('-created_at',)
