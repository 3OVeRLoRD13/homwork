from django.db import models
from django.contrib.auth.models import User


class Promotion(models.Model):
    description = models.TextField()
    discount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.description}-{self.discount}"

    __repr__ = __str__


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # circular dependency
    # '+' do no create reverse relation in product
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    last_update = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    __repr__ = __str__


class Product(models.Model):
    title = models.CharField(max_length=100)  # varchar(100)
    product_image = models.ImageField(default='product_default.png', upload_to='product_pics', null=True, blank=True)
    description = models.TextField()
    slug = models.SlugField(max_length=100)
    # 9999.99 max_digit: 6, decimal_places: 2
    price = models.DecimalField(max_digits=14, decimal_places=2)
    inventory = models.PositiveIntegerField()
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)
    likes = models.ManyToManyField(User, related_name="blog_products")
    last_update = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['title']),
        ]

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.title}"

    __repr__ = __str__
