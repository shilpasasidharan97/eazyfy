from email.policy import default
from random import choices
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phone_field import PhoneField
import uuid

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
    phone = models.CharField(max_length=15,null=True,blank=True)
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
    phone = models.CharField(max_length=15, null=True)
    photo = models.FileField(upload_to='franchise', null=True, blank=True)
    place = models.CharField(max_length=40, null=True)
    address = models.CharField(max_length=500, null=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class CutomerRegistration(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=500,null=True)
    phone_number = PhoneField(null=True)
    password = models.CharField(max_length=20,null=True)


    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = ("Customer")


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=15,unique=True)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, null=True, blank=True)
    pickup_boy = models.ForeignKey(PickUpBoy, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(CutomerRegistration, on_delete=models.CASCADE, null=True, blank=True)
    is_franchise= models.BooleanField(default=False)
    is_pickupboy=models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return str(self.phone_number)


class CutomerProfile(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE,related_name = 'profile')
    auth_token = models.CharField(max_length=100 ,blank = True, null = True)
    test_id = models.CharField(max_length=100 ,default = uuid.uuid4)
    forget_password_token = models.CharField(max_length=100, blank=True,null=True)


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

    def get_ram(self):
        return ModelSpecifications.objects.filter(Brand_model=self)

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

    class Meta:
        verbose_name_plural = ("Device Type")

    def __str__(self):
        return str(self.device_type)

#QUESTION ADDING

class Questions(models.Model):
    question_type = (('image_type', 'image_type'), ('Objective', 'Objective'))
    device_type = models.ForeignKey(DeviceType,on_delete = models.CASCADE,null = True,blank = True)
    model_question = models.ForeignKey(BrandModel,on_delete = models.CASCADE,null = True,blank = True)
    questions = models.CharField(max_length = 500,null = True)
    question_type = models.CharField(max_length = 15,choices = question_type)

    class Meta:
        verbose_name_plural = ("Questions")

    def __str__(self):
        return str(self.questions)

# IMAGE TYPE QUESTIONS

class QuestionOption(models.Model):
    question = models.ForeignKey(Questions,on_delete = models.CASCADE,null = True,blank = True)
    image_upload = models.FileField(upload_to = 'Question  Image',null = True)
    image_description = models.CharField(max_length = 500,null = True)

    class Meta:
        verbose_name_plural = ("Sub questions")

    def __str__(self):
        return str(self.image_description)


# OBJECTIVE TYPE DEDECTION

class Dedection(models.Model):
    questions = models.ForeignKey(Questions,on_delete = models.CASCADE,null = True, blank = True)
    model = models.ForeignKey(BrandModel,on_delete = models.CASCADE,null = True, blank = True)
    # dedection_amount = models.IntegerField(null = True, blank = True)
    dedection_amount_yes = models.IntegerField(null = True, blank = True)
    dedection_amount_no = models.IntegerField(null = True, blank = True)

    def get_subqust(self):
        return SubDedection.objects.filter(deduction=self) 

# IMAGE TYPE DEDECTION

class SubDedection(models.Model):
    questions = models.ForeignKey(Questions,on_delete = models.CASCADE,null = True, blank = True)
    qst_option = models.ForeignKey(QuestionOption, on_delete = models.CASCADE,null = True, blank = True)
    deduction = models.ForeignKey(Dedection, on_delete=models.CASCADE,null=True)
    model = models.ForeignKey(BrandModel,on_delete = models.CASCADE,null = True, blank = True)
    dedection_amount = models.IntegerField(null = True, blank = True)



# FRANCHISE WALLET

class FranchiseWallet(models.Model):
    franchise = models.ForeignKey(Franchise,on_delete = models.CASCADE,null = True, blank = True)
    wallet_amount = models.FloatField(null = True, blank = True, default=0)  
    last_paid_amount = models.FloatField(null = True, blank = True, default=0)
    date = models.DateTimeField(auto_now_add=True)

# ADMIN WALLET

class AdminWallet(models.Model):
    franchise = models.ForeignKey(Franchise,on_delete = models.CASCADE,null = True, blank = True)
    amount = models.FloatField(null = True, blank = True, default=0)  
    date = models.DateTimeField(auto_now_add=True)



class AdminSendRecord(models.Model):
    franchise = models.ForeignKey(Franchise,on_delete = models.CASCADE,null = True, blank = True)
    amount = models.FloatField(null = True, blank = True)  
    date = models.DateField()


# PICKUP BOY PAYMENT

class OrderPayment(models.Model):
    name = models.CharField(max_length=100)
    amound = models.CharField(max_length=100)
    paiment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)


class BannerImage(models.Model):
    banner = models.FileField(upload_to='gallery/', null=True, blank=True)


class Offer(models.Model):
    offer = models.FileField(upload_to='gallery/', null=True ,blank=True)



class Card(models.Model):
    card = models.FileField(upload_to='gallery/', null=True ,blank=True)


