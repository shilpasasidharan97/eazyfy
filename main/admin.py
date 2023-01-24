from django.contrib import admin
from .models import City, BannerImage, Offer, Team, Contact


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
