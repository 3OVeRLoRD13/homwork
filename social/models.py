from django.urls import reverse
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize


def cmp(a, b):
    return (a > b) - (a < b) 


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, null=True, blank=True, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, null=True, blank=True, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"user : {self.user_id}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=255, null=True, blank=True)
    post_image = models.ImageField(default='post_image_default.png', upload_to='posts_pics', null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    edited_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __cmp__(self, other):
        try:
            return cmp(self.created_at, other.created_at)
        except AttributeError:
            return cmp(self.created_at, other)
    
    def __str__(self):
        return f"{self.author}" + " Post"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.post_image.path)

        if img.height > 1024 or img.width > 1024 and not img.is_animated:
            output_size = (img.width / 2, img.height / 2)
            img.thumbnail(output_size)
            img.save(self.post_image.path)
    
    # check if has defualt image or not -------------------------------------------------------
    def has_default_image(self):
        if self.post_image.url == '/media/post_image_default.png':
            return True
        return False
    
    # Get absolute url ------------------------------------------------------------------------
    def get_absolute_url(self):
        return reverse('post_detail_view', kwargs={'pk': self.pk})
    
    # Return humanize date example(1 day and 3 hours ago) -------------------------------------
    def humanized_edit_date(self):
        return humanize.naturaltime(self.edited_at)

    # Return humanize date example(1 day and 3 hours ago) -------------------------------------
    def humanized_created_at(self):
        return humanize.naturaltime(self.created_at)

    # Check if a post is edited or not --------------------------------------------------------
    def is_edited(self):
        if self.created_at != self.edited_at:
            return True
        return False


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commented_post")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='+')
    text = models.TextField(max_length=255, null=True, blank=True)
    comment_image = models.ImageField(default='post_image_default.png', upload_to='comments_pics', null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='commentslikes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='commentsdislikes')
    edited_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __cmp__(self, other):
        try:
            return cmp(self.created_at, other.created_at)
        except AttributeError:
            return cmp(self.created_at, other)
    
    def __str__(self):
        return f"{self.author}" + " Comment"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.comment_image.path)

        if img.height > 1024 or img.width > 1024 and not img.is_animated:
            output_size = (img.width / 2, img.height / 2)
            img.thumbnail(output_size)
            img.save(self.comment_image.path)
    
    # Get all children  ---------------------------------------------------------------------------
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_at').all()

    # Comment replies count -----------------------------------------------------------------------
    def replies_count(self):
        return Comment.objects.filter(parent=self).count()
    
    # check if is parent or not -------------------------------------------------------------------
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    
    # check if has defualt image or not ----------------------------------------------------------
    def has_default_image(self):
        if self.comment_image.url == '/media/post_image_default.png':
            return True
        return False
    
    # Get absolute url ---------------------------------------------------------------------------
    def get_absolute_url(self):
        return reverse('post_detail_view', kwargs={'pk': self.pk})
    
    # Return humanize date example(1 day and 3 hours ago) ----------------------------------------
    def humanized_edit_date(self):
        return humanize.naturaltime(self.edited_at)

    # Return humanize date example(1 day and 3 hours ago) ----------------------------------------
    def humanized_created_at(self):
        return humanize.naturaltime(self.created_at)

    # Check if a comment is edited or not --------------------------------------------------------
    def is_edited(self):
        if self.created_at != self.edited_at:
            return True
        return False
    