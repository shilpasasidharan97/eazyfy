# Generated by Django 4.1.2 on 2023-01-25 01:49

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("official", "0005_userrequest_franchise")]

    operations = [
        migrations.AddField(
            model_name="userrequest", name="is_franchise_accepted", field=models.BooleanField(default=False)
        )
    ]
