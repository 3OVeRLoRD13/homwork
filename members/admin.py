from .models import UserProfile
from django.contrib import admin


# View UserProfile in admin page
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    list_display_links = ["id"]
    ordering = ["-created_at", "created_at"]
    list_per_page = 10
