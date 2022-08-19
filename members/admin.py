from django.contrib import admin
from .models import UserProfile, Post, FollowersCount


# View UserProfile in admin page
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    list_display_links = ["id"]
    ordering = ["-created_at", "created_at"]
    list_per_page = 10
    

# View FollowersCount posts in admin page
@admin.register(FollowersCount)
class FollowersCountAdmin(admin.ModelAdmin):
    list_display = ["id", "follower", "user"]
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
