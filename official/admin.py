from .models import AdminSendRecord
from .models import AdminWallet
from .models import Brand
from .models import BrandModel
from .models import CustomerProfile
from .models import CustomerRegistration
from .models import DeviceType
from .models import Franchise
from .models import FranchiseWallet
from .models import Variant
from .models import OrderPayment
from .models import PickUpBoy
from .models import Question
from .models import QuestionOption
from .models import User
from .models import UserReply
from .models import UserRequest
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
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0


@admin.register(BrandModel)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "image")
    search_fields = ("name",)
    list_filter = ("brand",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [VariantInline]


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ("brand_model", "RAM", "internal_storage", "color")
    search_fields = ("brand_model", "RAM", "internal_storage", "color")


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "question_type")
    search_fields = ("question",)
    inlines = [QuestionOptionInline]


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


@admin.register(UserReply)
class UserReplyAdmin(admin.ModelAdmin):
    list_display = ("question", "user_request", "option")
    list_filter = ("user_request",)


admin.site.register(DeviceType)
admin.site.register(UserRequest)
