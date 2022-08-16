from django.contrib import admin
from .models import UserProfile, Post


# View user profile in admin page
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    list_display_links = ["id"]
    search_fields = ["id", "user", "text"]
    ordering = ["-created_at", "created_at"]
    list_per_page = 10
    

# View user posts in admin page
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "edited_at", "created_at"]
    list_display_links = ["id"]
    search_fields = ["id", "author", "text"]
    ordering = ["-created_at", "created_at"]
    list_per_page = 10
