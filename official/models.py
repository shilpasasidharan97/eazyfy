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


