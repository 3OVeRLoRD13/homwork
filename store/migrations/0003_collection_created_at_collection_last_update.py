# Generated by Django 4.0.6 on 2022-07-30 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_collection_featured_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='last_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
