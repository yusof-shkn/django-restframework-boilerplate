from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')  # Fields displayed in the list view
    search_fields = ('title', 'content', 'user__email')  # Allow search by title, content, and user email
    list_filter = ('user', 'created_at')  # Filter options in the sidebar
    ordering = ('-created_at',)  # Order by created_at, descending (newest first)

admin.site.register(Post, PostAdmin)
