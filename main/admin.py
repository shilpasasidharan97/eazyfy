from .models import BannerImage
from .models import City
from .models import Contact
from .models import Offer
from .models import OtpModel
from .models import Team
from django.contrib import admin


@admin.register(OtpModel)
class OtpModelAdmin(admin.ModelAdmin):
    list_display = ["otp", "timestamp"]


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
