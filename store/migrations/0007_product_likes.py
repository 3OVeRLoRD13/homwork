# Generated by Django 4.0.6 on 2022-08-03 14:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0006_rename_descrition_promotion_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='likes',
            field=models.ManyToManyField(related_name='blog_products', to=settings.AUTH_USER_MODEL),
        ),
    ]