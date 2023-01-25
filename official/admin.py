from .models import AdminSendRecord
from .models import AdminWallet
from .models import Brand
from .models import BrandModel
from .models import CustomerProfile
from .models import CustomerRegistration
from .models import DeviceType
from .models import Franchise
from .models import FranchiseWallet
from .models import OrderPayment
from .models import PickUpBoy
from .models import Question
from .models import QuestionOption
from .models import User
from .models import UserReply
from .models import UserRequest
from .models import Variant
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("phone_number", "email", "password1", "password2", "is_franchise", "is_pickupboy", "is_customer")
        exclude = ("username",)


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            "phone_number",
            "email",
            "password",
            "is_franchise",
            "is_pickupboy",
            "is_customer",
            "is_staff",
            "is_active",
        )
        exclude = ("username",)


class MyUserAdmin(UserAdmin):
    USERNAME_FIELD = "phone_number"
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    # UserForm
    fieldsets = (
        (_("Authentication"), {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "is_franchise",
                    "is_pickupboy",
                    "is_customer",
                    "franchise",
                    "customer",
                    "pickup_boy",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    list_display = ("phone_number", "email", "is_franchise", "is_pickupboy", "is_customer", "is_staff", "is_active")
    search_fields = ("phone_number", "email")
    list_filter = ("is_franchise", "is_pickupboy", "is_customer", "is_staff", "is_active")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2", "is_franchise", "is_pickupboy", "is_customer"),
            },
        ),
    )
    ordering = ("phone_number",)
    exclude = ("username",)


admin.site.register(User, MyUserAdmin)


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    pass


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


@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phonemodel",
        "is_submitted",
        "is_assigned_to_franchise",
        "is_franchise_accepted",
        "is_assigned_to_pickup",
        "is_quoted",
    )
    list_filter = (
        "user",
        "phonemodel",
        "is_submitted",
        "is_assigned_to_franchise",
        "is_franchise_accepted",
        "is_assigned_to_pickup",
        "is_quoted",
    )
    readonly_fields = ("request_id",)
