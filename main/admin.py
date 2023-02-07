from .models import BannerImage
from .models import City
from .models import Contact
from .models import Offer
from .models import PhoneOTP
from .models import Team
from django.contrib import admin


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ["phone_number", "otp", "timestamp"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["city_name"]


@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ["offer"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "designation", "description"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "subject", "message"]
