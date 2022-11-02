from random import choices
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phone_field import PhoneField

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,phone_number,password=None,**extra_fields):

        if not phone_number:
            raise ValueError('User must have a phone_number')
        user = self.model(phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        if user:
            return user
    def create_superuser(self,phone_number,password=None,**extra_fields):

        if not phone_number:
            raise ValueError('User must have a email')
        user = self.model(phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff   = True
        user.save(using=self._db)
        return user






class Franchise(models.Model):
    franchise_id = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=40, null=True)
    email = models.EmailField(null=True)
    phone = PhoneField(null=True)
    photo = models.FileField(upload_to='franchise', null=True, blank=True)
    address = models.CharField(max_length=500, null=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class PickUpBoy(models.Model):
    franchise = models.ForeignKey(Franchise,on_delete=models.CASCADE)
    pickup_id = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=40, null=True)
    email = models.EmailField(null=True)
    phone = PhoneField(null=True)
    photo = models.FileField(upload_to='franchise', null=True, blank=True)
    place = models.CharField(max_length=40, null=True)
    address = models.CharField(max_length=500, null=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

class User(AbstractUser):
    username = None
    phone_number = PhoneField(unique=True)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, null=True, blank=True)
    pickup_boy = models.ForeignKey(PickUpBoy, on_delete=models.CASCADE, null=True, blank=True)
    is_franchise= models.BooleanField(default=False)
    is_pickupboy=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return str(self.phone_number)



class Brand(models.Model):
    image = models.FileField(upload_to='Brand', null=True)
    name = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = ("Brand")

    def __str__(self):
        return str(self.name)


class BrandModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.FileField(upload_to='Brand Model', null=True)
    name = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = ("Brand Model")

    def __str__(self):
        return str(self.name)


class ModelSpecifications(models.Model):
    Brand_model = models.ForeignKey(BrandModel, on_delete=models.CASCADE)
    RAM = models.CharField(max_length=100, null="True")
    color = models.CharField(max_length=30, null=True)
    internal_storage = models.CharField(max_length=30, null=True)
    year = models.IntegerField(null=True)
    price = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = ("Model Specifications")



class DeviceType(models.Model):
    device_choices =  (('Mobile', 'Mobile'), ('TV', 'TV'),('Laptop','Laptop'))
    device_type = models.CharField(max_length = 10,choices = device_choices)

class Questions(models.Model):
    question_type = (('image_type', 'image_type'), ('Objective', 'Objective'))
    device_type = models.ForeignKey(DeviceType,on_delete = models.CASCADE,null = True,blank = True)
    questions = models.CharField(max_length = 500,null = True)
    question_type = models.CharField(max_length = 15,choices = question_type)

class Dedection(models.Model):
    questions = models.ForeignKey(Questions,on_delete = models.CASCADE,null = True, blank = True)
    spec = models.ForeignKey(ModelSpecifications,on_delete = models.CASCADE,null = True, blank = True)
    dedection_amount = models.IntegerField(null = True, blank = True)
