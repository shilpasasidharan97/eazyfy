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


class OtpModel(models.Model):
    otp = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.otp)
