import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from phone_field import PhoneField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("User must have a phone_number")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        if user:
            return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("User must have a email")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    franchise = models.ForeignKey("Franchise", on_delete=models.CASCADE, null=True, blank=True)
    pickup_boy = models.ForeignKey("PickUpBoy", on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey("CustomerRegistration", on_delete=models.CASCADE, null=True, blank=True)
    is_franchise = models.BooleanField(default=False)
    is_pickupboy = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)


class Franchise(models.Model):
    franchise_id = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15, blank=True)
    photo = models.FileField(upload_to="franchise", null=True, blank=True)
    address = models.CharField(max_length=500)
    password = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class PickUpBoy(models.Model):
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    pickup_id = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15)
    photo = models.FileField(upload_to="franchise", null=True, blank=True)
    place = models.CharField(max_length=40)
    address = models.CharField(max_length=500)
    password = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class CustomerRegistration(models.Model):
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=500, null=True)
    phone_number = PhoneField(null=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Customer"


class CustomerProfile(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="profile")
    auth_token = models.CharField(max_length=100, blank=True)
    test_id = models.CharField(max_length=100, default=uuid.uuid4)
    forget_password_token = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.user)


class Brand(models.Model):
    image = models.FileField(upload_to="Brand", null=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Brand"

    def get_brand_models(self):
        return BrandModel.objects.filter(brand=self)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)


class BrandModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.FileField(upload_to="models/")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def get_varients(self):
        return ModelSpecifications.objects.filter(brand_model=self)

    def __str__(self):
        return str(self.name)


class ModelSpecifications(models.Model):
    brand_model = models.ForeignKey(BrandModel, on_delete=models.CASCADE)
    RAM = models.CharField(max_length=100, null="True")
    color = models.CharField(max_length=30)
    internal_storage = models.CharField(max_length=30)
    year = models.IntegerField(null=True)
    price = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = "Model Specifications"

    def __str__(self):
        return str(self.brand_model)


class DeviceType(models.Model):
    device_choices = (("Mobile", "Mobile"), ("TV", "TV"), ("Laptop", "Laptop"))
    device_type = models.CharField(max_length=10, choices=device_choices)

    class Meta:
        verbose_name_plural = "Device Type"

    def __str__(self):
        return str(self.device_type)


class FranchiseWallet(models.Model):
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, null=True, blank=True)
    wallet_amount = models.FloatField(null=True, blank=True, default=0)
    last_paid_amount = models.FloatField(null=True, blank=True, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.franchise)


class AdminWallet(models.Model):
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.franchise)


class AdminSendRecord(models.Model):
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        return str(self.franchise)


class OrderPayment(models.Model):
    name = models.CharField(max_length=100)
    amound = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# survey models
class QuestionOption(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to="Question Image", blank=True, null=True)
    text = models.CharField(max_length=500)
    identifier = models.CharField(max_length=500, blank=True, null=True, help_text="Eg: Able to Make and Receive Calls")

    class Meta:
        verbose_name_plural = "Question Options"

    def __str__(self):
        return f"{self.question} - {self.text}"


class Question(models.Model):
    question_type_choices = (("image", "Image"), ("Objective", "Objective"), ("MCQ", "MCQ"))

    question_type = models.CharField(max_length=15, choices=question_type_choices)
    question = models.CharField(
        max_length=500, blank=True, null=True, help_text="Eg: Are you able to make and receive calls?"
    )
    subtext = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Eg: Check your device for cellular network connectivity issues.",
    )

    class Meta:
        verbose_name_plural = "Question"

    def get_options(self):
        return QuestionOption.objects.filter(question=self)

    def __str__(self):
        return str(self.question)


class UserRequest(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    phonemodel = models.ForeignKey(ModelSpecifications, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    final_amount = models.FloatField(default=0)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class UserReply(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    user_request = models.ForeignKey("UserRequest", on_delete=models.CASCADE)
    option = models.ForeignKey("QuestionOption", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user_request)
