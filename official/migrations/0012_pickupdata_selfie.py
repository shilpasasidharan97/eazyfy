# Generated by Django 4.1.2 on 2023-01-25 22:08

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("official", "0011_pickupdata")]

    operations = [
        migrations.AddField(
            model_name="pickupdata",
            name="selfie",
            field=models.ImageField(blank=True, null=True, upload_to="selfie", verbose_name="Selfie with Customer"),
        )
    ]
