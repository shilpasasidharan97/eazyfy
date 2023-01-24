# Generated by Django 4.1.2 on 2023-01-24 20:01

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("official", "0008_remove_variant_price_variant_max_price_and_more")]

    operations = [
        migrations.RemoveField(model_name="variant", name="year"),
        migrations.AlterField(
            model_name="variant", name="max_price", field=models.DecimalField(decimal_places=2, max_digits=10)
        ),
        migrations.AlterField(
            model_name="variant", name="min_price", field=models.DecimalField(decimal_places=2, max_digits=10)
        ),
    ]
