from .models import AdminSendRecord
from .models import AdminWallet
from .models import BannerImage
from .models import Brand
from .models import BrandModel
from .models import CutomerRegistration
from .models import Deduction
from .models import DeviceType
from .models import Franchise
from .models import FranchiseWallet
from .models import ModelSpecifications
from .models import Offer
from .models import PickUpBoy
from .models import QuestionOption
from .models import Questions
from .models import SubDeduction
from .models import User
from django.contrib import admin


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("franchise", "pickup_boy", "customer")
    search_fields = ("franchise", "pickup_boy")


admin.site.register(User, UserAdmin)


class FranchiseAdmin(admin.ModelAdmin):
    list_display = ("franchise_id", "name", "phone")
    search_fields = ("franchise_id", "name", "phone")


admin.site.register(Franchise, FranchiseAdmin)


class PickUpBoyAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "franchise")
    search_fields = ("name", "phone", "franchise")


admin.site.register(PickUpBoy, PickUpBoyAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "image")
    search_fields = ("name", "image")


admin.site.register(Brand, BrandAdmin)


class BrandModelAdmin(admin.ModelAdmin):
    list_display = ("brand", "name", "image")
    search_fields = ("brand", "name", "image")


admin.site.register(BrandModel, BrandModelAdmin)


class ModelSpecificationsAdmin(admin.ModelAdmin):
    list_display = ("brand_model", "RAM", "internal_storage", "color", "year")
    search_fields = ("brand_model", "RAM", "internal_storage", "color", "year")


admin.site.register(ModelSpecifications, ModelSpecificationsAdmin)


admin.site.register(DeviceType)


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("id", "questions", "question_type")
    search_fields = ("questions",)


admin.site.register(Questions, QuestionsAdmin)


class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ("question_id", "question", "image_description", "image_upload")
    search_fields = ("questions",)


admin.site.register(QuestionOption, QuestionOptionAdmin)


class DeductionAdmin(admin.ModelAdmin):
    list_display = ("questions", "model", "deduction_amount_yes", "deduction_amount_no")
    search_fields = ("questions", "model", "deduction_amount_yes", "deduction_amount_no")


admin.site.register(Deduction, DeductionAdmin)


class CutomerRegistrationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone_number")


admin.site.register(CutomerRegistration, CutomerRegistrationAdmin)


class FranchiseWalletAdmin(admin.ModelAdmin):
    list_display = ("franchise", "wallet_amount", "date")
    search_fields = ("franchise", "wallet_amount", "date")


admin.site.register(FranchiseWallet, FranchiseWalletAdmin)


class AdminWalletAdmin(admin.ModelAdmin):
    list_display = ("franchise", "amount", "date")
    search_fields = ("franchise", "amount", "date")


admin.site.register(AdminWallet, AdminWalletAdmin)


class AdminSendRecordAdmin(admin.ModelAdmin):
    list_display = ("franchise", "amount", "date")
    search_fields = ("franchise", "amount", "date")


admin.site.register(AdminSendRecord, AdminSendRecordAdmin)


class SubDeductionAdmin(admin.ModelAdmin):
    list_display = ("questions", "model", "deduction_amount")
    search_fields = ("questions", "model", "deduction_amount")


admin.site.register(SubDeduction, SubDeductionAdmin)

admin.site.register(BannerImage)
admin.site.register(Offer)
