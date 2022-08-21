from django.contrib import admin
from .models import Post, UserFollowing


# View FollowersCount posts in admin page
@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ["id"]
    list_display_links = ["id"]
    list_per_page = 10


# View User Posts in admin page
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "edited_at", "created_at"]
    exclude = ('author_username',)
    list_display_links = ["id"]
    ordering = ["-created_at", "created_at"]
    list_per_page = 10
