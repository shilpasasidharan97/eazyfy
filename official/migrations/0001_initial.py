# Generated by Django 4.1.2 on 2022-12-30 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phone_field.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [("auth", "0012_alter_user_first_name_max_length")]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False, help_text="Designates that this user has all permissions without explicitly assigning them.", verbose_name="superuser status"
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("email", models.EmailField(blank=True, max_length=150, null=True)),
                ("phone_number", models.CharField(max_length=15, unique=True)),
                ("is_franchise", models.BooleanField(default=False)),
                ("is_pickupboy", models.BooleanField(default=False)),
                ("is_customer", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
            ],
            options={"verbose_name": "user", "verbose_name_plural": "users", "abstract": False},
        ),
        migrations.CreateModel(
            name="BannerImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("banner", models.FileField(blank=True, null=True, upload_to="gallery/")),
            ],
        ),
        migrations.CreateModel(
            name="Brand",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.FileField(null=True, upload_to="Brand")),
                ("name", models.CharField(default="", max_length=100)),
            ],
            options={"verbose_name_plural": "Brand"},
        ),
        migrations.CreateModel(
            name="BrandModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.FileField(null=True, upload_to="Brand Model")),
                ("name", models.CharField(default="", max_length=100)),
                ("brand", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="official.brand")),
            ],
        ),
        migrations.CreateModel(
            name="CustomerRegistration",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, default="", max_length=50)),
                ("email", models.EmailField(max_length=500, null=True)),
                ("phone_number", phone_field.models.PhoneField(max_length=31, null=True)),
                ("password", models.CharField(default="", max_length=20)),
            ],
            options={"verbose_name_plural": "Customer"},
        ),
        migrations.CreateModel(
            name="Deduction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deduction_amount_yes", models.IntegerField(blank=True, null=True)),
                ("deduction_amount_no", models.IntegerField(blank=True, null=True)),
                ("model", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.brandmodel")),
            ],
        ),
        migrations.CreateModel(
            name="DeviceType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("device_type", models.CharField(choices=[("Mobile", "Mobile"), ("TV", "TV"), ("Laptop", "Laptop")], max_length=10)),
            ],
            options={"verbose_name_plural": "Device Type"},
        ),
        migrations.CreateModel(
            name="Franchise",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("franchise_id", models.CharField(default="", max_length=20)),
                ("name", models.CharField(default="", max_length=40)),
                ("email", models.EmailField(max_length=254, null=True)),
                ("phone", models.CharField(blank=True, default="", max_length=15)),
                ("photo", models.FileField(blank=True, null=True, upload_to="franchise")),
                ("address", models.CharField(default="", max_length=500)),
                ("password", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="ModelSpecifications",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("RAM", models.CharField(max_length=100, null="True")),
                ("color", models.CharField(default="", max_length=30)),
                ("internal_storage", models.CharField(default="", max_length=30)),
                ("year", models.IntegerField(null=True)),
                ("price", models.FloatField(null=True)),
                ("brand_model", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="official.brandmodel")),
            ],
            options={"verbose_name_plural": "Model Specifications"},
        ),
        migrations.CreateModel(
            name="Offer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("offer", models.FileField(blank=True, null=True, upload_to="gallery/")),
            ],
        ),
        migrations.CreateModel(
            name="OrderPayment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("amound", models.CharField(max_length=100)),
                ("payment_id", models.CharField(max_length=100)),
                ("paid", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="QuestionOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image_upload", models.FileField(null=True, upload_to="Question  Image")),
                ("image_description", models.CharField(default="", max_length=500)),
            ],
            options={"verbose_name_plural": "Sub questions"},
        ),
        migrations.CreateModel(
            name="Questions",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("questions", models.CharField(default="", max_length=500)),
                ("question_type", models.CharField(choices=[("image_type", "image_type"), ("Objective", "Objective")], max_length=15)),
                ("brand_model", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.brandmodel")),
                ("device_type", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.devicetype")),
            ],
            options={"verbose_name_plural": "Questions"},
        ),
        migrations.CreateModel(
            name="SubDeduction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deduction_amount", models.IntegerField(blank=True, null=True)),
                ("deduction", models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="official.deduction")),
                ("model", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.brandmodel")),
                ("qst_option", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.questionoption")),
                ("questions", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.questions")),
            ],
        ),
        migrations.CreateModel(
            name="UserQuestionAnswerOptions",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("answer", models.BooleanField(default=False)),
                ("is_subqst", models.BooleanField(default=False)),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="official.deduction")),
            ],
        ),
        migrations.CreateModel(
            name="UserQuestionAnswer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("final_amount", models.FloatField(default=0)),
                ("phonemodel", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="official.modelspecifications")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="SubQstAnswer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("answer", models.BooleanField(default=False)),
                ("main_question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="official.userquestionansweroptions")),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="official.subdeduction")),
            ],
        ),
        migrations.AddField(
            model_name="questionoption", name="question", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.questions")
        ),
        migrations.CreateModel(
            name="PickUpBoy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("pickup_id", models.CharField(default="", max_length=20)),
                ("name", models.CharField(default="", max_length=40)),
                ("email", models.EmailField(max_length=254, null=True)),
                ("phone", models.CharField(default="", max_length=15)),
                ("photo", models.FileField(blank=True, null=True, upload_to="franchise")),
                ("place", models.CharField(default="", max_length=40)),
                ("address", models.CharField(default="", max_length=500)),
                ("password", models.CharField(max_length=20)),
                ("franchise", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="official.franchise")),
            ],
        ),
        migrations.CreateModel(
            name="FranchiseWallet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("wallet_amount", models.FloatField(blank=True, default=0, null=True)),
                ("last_paid_amount", models.FloatField(blank=True, default=0, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("franchise", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.franchise")),
            ],
        ),
        migrations.AddField(
            model_name="deduction", name="questions", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.questions")
        ),
        migrations.CreateModel(
            name="CustomerProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("auth_token", models.CharField(blank=True, default="", max_length=100)),
                ("test_id", models.CharField(default=uuid.uuid4, max_length=100)),
                ("forget_password_token", models.CharField(blank=True, default="", max_length=100)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="AdminWallet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.FloatField(blank=True, default=0, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("franchise", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.franchise")),
            ],
        ),
        migrations.CreateModel(
            name="AdminSendRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.FloatField(blank=True, null=True)),
                ("date", models.DateField()),
                ("franchise", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.franchise")),
            ],
        ),
        migrations.AddField(
            model_name="user", name="customer", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.customerregistration")
        ),
        migrations.AddField(
            model_name="user", name="franchise", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.franchise")
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user", name="pickup_boy", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="official.pickupboy")
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
