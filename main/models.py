from .choices import COUNTRY_CODE_CHOICES
from django.core.exceptions import ValidationError
from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="city_icons")

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.city_name


class BannerImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to="banners/")
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Offer(models.Model):
    offer = models.FileField(upload_to="offers/")

    def __str__(self):
        return str(self.offer)


class Team(models.Model):
    image = models.FileField(upload_to="team/")
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return str(self.name)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return str(self.name)


class PhoneOTP(models.Model):
    def validate_only_numbers(value):
        if not value.isdigit():
            raise ValidationError("Phone number must contain only numbers.")

    country_code = models.CharField(max_length=10, default="+91", choices=COUNTRY_CODE_CHOICES)
    phone_number = models.CharField(max_length=12, validators=[validate_only_numbers])
    otp = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.otp)

    class Meta:
        verbose_name = "Phone OTP"
        verbose_name_plural = "Phone OTPs"
        ordering = ["-timestamp"]
