# Generated by Django 4.1.2 on 2023-01-24 16:42

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("official", "0005_brandmodel_slug_alter_brandmodel_image")]

    operations = [
        migrations.AlterField(model_name="brandmodel", name="slug", field=models.SlugField(max_length=100, unique=True))
    ]
