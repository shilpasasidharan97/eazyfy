# Generated by Django 4.1.2 on 2022-12-30 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("official", "0005_rename_model_question_questions_brand_model")]

    operations = [migrations.RenameField(model_name="orderpayment", old_name="paiment_id", new_name="payment_id")]
