from django.contrib import admin
from . models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('franchise', 'pickup_boy')
    search_fields = ('franchise', 'pickup_boy')


admin.site.register(User, UserAdmin)

class FranchiseAdmin(admin.ModelAdmin):
    list_display = ('franchise_id', 'name','phone' )
    search_fields = ('franchise_id', 'name','phone')


admin.site.register(Franchise, FranchiseAdmin)


class PickUpBoyAdmin(admin.ModelAdmin):
    list_display = ('name','phone', 'franchise' )
    search_fields = ('name','phone', 'franchise')


admin.site.register(PickUpBoy, PickUpBoyAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name','image' )
    search_fields = ('name','image')


admin.site.register(Brand, BrandAdmin)


class BrandModelAdmin(admin.ModelAdmin):
    list_display = ('brand','name','image' )
    search_fields = ('brand','name','image')


admin.site.register(BrandModel, BrandModelAdmin)


class ModelSpecificationsAdmin(admin.ModelAdmin):
    list_display = ('Brand_model','RAM', 'internal_storage', 'color', 'year' )
    search_fields = ('Brand_model','RAM', 'internal_storage', 'color', 'year')


admin.site.register(ModelSpecifications, ModelSpecificationsAdmin)


admin.site.register(DeviceType)

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('questions','question_type' )
    search_fields = ('questions',)


admin.site.register(Questions, QuestionsAdmin)


class DedectionAdmin(admin.ModelAdmin):
    list_display = ('spec','dedection_amount' )
    search_fields = ('spec','dedection_amount')


admin.site.register(Dedection, DedectionAdmin)


admin.site.register(QuestionOption)