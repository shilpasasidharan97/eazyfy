import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from phone_field import PhoneField


DEVICE_CATEGORY = (
    ("mobile", "Mobile"),
    ("laptop", "Laptop"),
    ("tablet", "Tablet"),
    ("accessories", "Accessories"),
    ("camera", "Camera"),
    ("earbud", "Earbud"),
    ("headphone", "Headphone"),
    ("smartwatch", "Smartwatch"),
    ("smartband", "Smartband"),
)


class User(AbstractUser):
    usertype = models.CharField(
        max_length=20,
        choices=(("franchise", "Franchise"), ("pickupboy", "Pickupboy"), ("customer", "Customer")),
        default="customer",
    )

    def __str__(self):
        if self.first_name and self.last_name:
            return str(self.first_name + " " + self.last_name)
        elif self.first_name:
            return str(self.first_name)
        else:
            return str(self.username)


class Franchise(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, blank=True, null=True, related_name="franchise")
    franchise_id = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15, blank=True)
    photo = models.FileField(upload_to="franchise", null=True, blank=True)
    address = models.CharField(max_length=500)

    def get_credits(self):
        return FranchiseWallet.objects.filter(franchise=self, type="to_franchise")

    def get_debits(self):
        return FranchiseWallet.objects.filter(franchise=self, type="to_admin")

    def get_total_credits(self):
        return sum([i.amount for i in self.get_credits()])

    def get_total_debits(self):
        return sum([i.amount for i in self.get_debits()])

    def get_balance(self):
        return self.get_total_credits() - self.get_total_debits()

    def __str__(self):
        return str(self.name)


class PickUpBoy(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, blank=True, null=True, related_name="pickupboy")
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    pickup_id = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15)
    photo = models.FileField(upload_to="franchise", null=True, blank=True)
    place = models.CharField(max_length=40)
    address = models.CharField(max_length=500)

    def __str__(self):
        return str(self.name)


class Customer(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, blank=True, null=True, related_name="customer")
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone_number = PhoneField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Brand(models.Model):
    image = models.FileField(upload_to="Brand", null=True, blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    references = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Brand"

    def get_mobile_models(self):
        return BrandModel.objects.filter(brand=self, category="mobile")

    def get_laptop_models(self):
        return BrandModel.objects.filter(brand=self, category="laptop")

    def get_tablet_models(self):
        return BrandModel.objects.filter(brand=self, category="tablet")

    def get_accessories_models(self):
        return BrandModel.objects.filter(brand=self, category="accessories")

    def get_camera_models(self):
        return BrandModel.objects.filter(brand=self, category="camera")

    def get_earbud_models(self):
        return BrandModel.objects.filter(brand=self, category="earbud")

    def get_headphone_models(self):
        return BrandModel.objects.filter(brand=self, category="headphone")

    def get_smartwatch_models(self):
        return BrandModel.objects.filter(brand=self, category="smartwatch")

    def get_smartband_models(self):
        return BrandModel.objects.filter(brand=self, category="smartband")

    def devices_count(self):
        return self.get_mobile_models().count()

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BrandModel(models.Model):
    def get_image_path(instance, filename):
        return "models/{0}/{1}".format(instance.brand.slug, filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_image_path)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_mostselling = models.BooleanField(default=False)
    category = models.CharField(max_length=100, choices=DEVICE_CATEGORY, default="mobile")

    def get_variants(self):
        return Variant.objects.filter(brand_model=self)

    def get_absolute_url(self):
        return reverse("main:device_page", kwargs={"slug": self.slug})

    class Meta:
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Variant(models.Model):
    brand_model = models.ForeignKey(BrandModel, on_delete=models.CASCADE)
    RAM = models.CharField(max_length=100, null="True")
    color = models.CharField(max_length=30)
    internal_storage = models.CharField(max_length=30)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)

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
    amount = models.FloatField(null=True, blank=True, default=0)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=100, choices=(("to_franchise", "to_franchise"), ("to_admin", "to_admin")), default="to_franchise"
    )

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
    image = models.FileField(upload_to="question_images", blank=True, null=True)
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
    def get_request_id():
        return str(uuid.uuid4()).upper()[-8:]

    request_id = models.CharField(max_length=100, default=get_request_id, editable=False)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    phonemodel = models.ForeignKey(Variant, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    final_amount = models.FloatField(default=0)
    is_submitted = models.BooleanField(default=False)
    is_assigned_to_franchise = models.BooleanField(default=False)
    is_franchise_accepted = models.BooleanField(default=False)
    is_assigned_to_pickup = models.BooleanField(default=False)
    is_quoted = models.BooleanField(default=False)
    franchise = models.ForeignKey("Franchise", on_delete=models.CASCADE, null=True, blank=True)
    pickupboy = models.ForeignKey("PickUpBoy", on_delete=models.CASCADE, null=True, blank=True)
    prefferred_contact = models.CharField(max_length=100, null=True, blank=True)

    name = models.CharField("Name of person who will deliver the product", max_length=100, null=True, blank=True)
    phone = models.CharField(
        "Contact number of person who will deliver the product", max_length=100, null=True, blank=True
    )
    address = models.TextField("Address of person who will deliver the product", null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=100,
        choices=(("pending", "pending"), ("complete", "complete"), ("requote", "requote"), ("fail", "fail")),
        default="pending",
    )

    def get_replies(self):
        return UserReply.objects.filter(user_request=self)

    def __str__(self):
        return str(self.customer)


class UserReply(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    user_request = models.ForeignKey("UserRequest", on_delete=models.CASCADE)
    option = models.ManyToManyField("QuestionOption", blank=True)

    def __str__(self):
        return str(self.user_request)


class PickupData(models.Model):
    user_request = models.OneToOneField("UserRequest", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100,
        choices=(("pending", "pending"), ("complete", "complete"), ("requote", "requote"), ("fail", "fail")),
        default="pending",
    )
    imei_number = models.CharField(max_length=100, null=True, blank=True)
    front_image = models.ImageField("front side of the phone", upload_to="pickup/FrontImage", null=True, blank=True)
    back_image = models.ImageField("back side of the phone", upload_to="pickup/BackImage", null=True, blank=True)
    top_image = models.ImageField("top side of the phone", upload_to="pickup/TopSide", null=True, blank=True)
    bottom_image = models.ImageField("bottom side of the phone", upload_to="pickup/BottomSide", null=True, blank=True)
    right_image = models.ImageField("right side of the phone", upload_to="pickup/RightSide", null=True, blank=True)
    left_image = models.ImageField("left side of the phone", upload_to="pickup/LeftSide", null=True, blank=True)
    selfie_image = models.ImageField("Selfie with Customer", upload_to="pickup/Selfie", null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.user_request)

    def save(self, *args, **kwargs):
        self.user_request.status = self.status
        self.user_request.save()
        super().save(*args, **kwargs)
