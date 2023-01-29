from .models import Brand
from .models import BrandModel
from .models import Customer
from .models import DeviceType
from .models import Franchise
from .models import FranchiseWallet
from .models import OrderPayment
from .models import PickUpBoy
from .models import PickupData
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
from import_export.admin import ImportExportActionModelAdmin


class MyUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ("email", "is_staff", "is_active", "is_superuser")
    list_filter = ("email", "is_staff", "is_active", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "password", "usertype")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_staff", "is_active", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, MyUserAdmin)


@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    autocomplete_fields = ("user",)
    list_display = ("franchise_id", "name", "phone")
    search_fields = ("franchise_id", "name", "phone")


@admin.register(PickUpBoy)
class PickUpBoyAdmin(admin.ModelAdmin):
    autocomplete_fields = ("user", "franchise")
    list_display = ("name", "phone", "franchise")
    search_fields = ("name", "phone", "franchise")


@admin.register(Brand)
class BrandAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "devices_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0


@admin.register(BrandModel)
class BrandModelAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "brand", "category", "id")
    list_editable = ("category",)
    search_fields = ("name", "slug")
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


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    autocomplete_fields = ("user",)
    list_display = ("user", "name", "email", "phone_number")


@admin.register(FranchiseWallet)
class FranchiseWalletAdmin(admin.ModelAdmin):
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
        "customer",
        "phonemodel",
        "is_submitted",
        "is_assigned_to_franchise",
        "is_franchise_accepted",
        "is_assigned_to_pickup",
        "is_quoted",
    )
    list_filter = (
        "customer",
        "phonemodel",
        "is_submitted",
        "is_assigned_to_franchise",
        "is_franchise_accepted",
        "is_assigned_to_pickup",
        "is_quoted",
        "status",
    )
    readonly_fields = ("request_id", "status")


@admin.register(PickupData)
class PickupDataAdmin(admin.ModelAdmin):
    pass
