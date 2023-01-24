# Generated by Django 4.1.2 on 2023-01-24 16:41

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("main", "0007_alter_bannerimage_image_alter_offer_offer_and_more")]

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=100)),
                ("subject", models.CharField(max_length=100)),
                ("message", models.TextField()),
            ],
        )
    ]
