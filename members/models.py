from django.urls import reverse
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


class FollowersCount(models.Model):
    follower = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    
    def __str__(self):
        return self.user


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_username = models.CharField(max_length=255)
    text = models.TextField(max_length=255, null=True, blank=True)
    post_image = models.ImageField(default='post_image_default.png', upload_to='posts_pics', null=True, blank=True)
    edited_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author}" + " Post"
    
    def save(self, *args, **kwargs):
        self.author_username = str(self.author)
        super().save(*args, **kwargs)
        
        img = Image.open(self.post_image.path)

        if img.height > 1024 or img.width > 1024 and not img.is_animated:
            output_size = (img.width / 2, img.height / 2)
            img.thumbnail(output_size)
            img.save(self.post_image.path)
        
        #super(Post, self).save(*args, **kwargs)
    
    def has_default_image(self):
        if self.post_image.url == '/media/post_image_default.png':
            return True
        return False
    
    def get_absolute_url(self):
        return reverse('post_detail_view', kwargs={'pk': self.pk})
    
    # Return humanize date example(1 day and 3 hours ago) 
    def humanized_edit_date(self):
        return humanize.naturaltime(self.edited_at)

    # Return humanize date example(1 day and 3 hours ago)
    def humanized_created_at(self):
        return humanize.naturaltime(self.created_at)

    # Check if a post is edited or not
    def is_edited(self):
        if self.created_at != self.edited_at:
            return True
        return False
