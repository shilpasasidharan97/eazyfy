from .models import AdminSendRecord
from .models import AdminWallet
from .models import BannerImage
from .models import Brand
from .models import BrandModel
from .models import CustomerProfile
from .models import CustomerRegistration
from .models import DeviceType
from .models import Franchise
from .models import FranchiseWallet
from .models import ModelSpecifications
from .models import Offer
from .models import OrderPayment
from .models import PickUpBoy
from .models import QuestionOption
from .models import Questions
from .models import User
from django.contrib import admin


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("franchise", "pickup_boy", "customer")
    search_fields = ("franchise", "pickup_boy")


@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    list_display = ("franchise_id", "name", "phone")
    search_fields = ("franchise_id", "name", "phone")


@admin.register(PickUpBoy)
class PickUpBoyAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "franchise")
    search_fields = ("name", "phone", "franchise")


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "image")
    search_fields = ("name", "image")


@admin.register(BrandModel)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ("brand", "name", "image")
    search_fields = ("brand", "name", "image")


@admin.register(ModelSpecifications)
class ModelSpecificationsAdmin(admin.ModelAdmin):
    list_display = ("brand_model", "RAM", "internal_storage", "color", "year")
    search_fields = ("brand_model", "RAM", "internal_storage", "color", "year")


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("id", "questions", "question_type")
    search_fields = ("questions",)


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ("question_id", "question", "image_description", "image_upload")
    search_fields = ("questions",)


@admin.register(CustomerRegistration)
class CustomerRegistrationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone_number")


@admin.register(FranchiseWallet)
class FranchiseWalletAdmin(admin.ModelAdmin):
    list_display = ("franchise", "wallet_amount", "date")
    search_fields = ("franchise", "wallet_amount", "date")


@admin.register(AdminWallet)
class AdminWalletAdmin(admin.ModelAdmin):
    list_display = ("franchise", "amount", "date")
    search_fields = ("franchise", "amount", "date")


@admin.register(AdminSendRecord)
class AdminSendRecordAdmin(admin.ModelAdmin):
    list_display = ("franchise", "amount", "date")
    search_fields = ("franchise", "amount", "date")


admin.site.register(BannerImage)
admin.site.register(Offer)
admin.site.register(DeviceType)
