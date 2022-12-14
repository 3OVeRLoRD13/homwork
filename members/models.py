from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='default.png', upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(max_length=150, null=True, blank=True)
    birth_date = models.DateField(max_length=8, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.user.username} Profile"            
    
    def get_last_update_date(self):
        return humanize.naturaltime(self.last_update)

    def get_created_at_date(self):
        return humanize.naturaltime(self.created_at)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_image.path)

        if img.height > 512 or img.width > 512:
            output_size = (img.width / 2, img.height / 2)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)
