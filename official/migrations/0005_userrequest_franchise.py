# Generated by Django 4.1.2 on 2023-01-25 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("official", "0004_alter_userrequest_request_id")]

    operations = [
        migrations.AddField(
            model_name="userrequest",
            name="franchise",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.franchise"
            ),
        )
    ]
