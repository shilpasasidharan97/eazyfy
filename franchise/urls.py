from django.urls import path
from . import views

app_name = 'franchise'

urlpatterns = [
    path('header',views.header,name="header"),

    path('',views.index,name="index"),
    path('profile',views.profile,name="profile"),
    path('add-pickupboy',views.add_pickupboy,name="add-pickupboy"),
    path('order',views.order,name="order"),

    path('deletepickupboy/<int:id>',views.Deletepickupboy, name='deletepickupboy'),
    path('editform/<int:id>',views.editform,name='editform'),
    path('getprofiledata/<int:id>',views.getprofiledata,name='getprofiledata'),

]