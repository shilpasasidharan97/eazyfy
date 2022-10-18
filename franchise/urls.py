from django.urls import path
from . import views

app_name = 'franchise'

urlpatterns = [
    path('',views.index,name="index"),
    path('profile',views.profile,name="profile"),
    path('add-pickupboy',views.add_pickupboy,name="add-pickupboy"),
    path('order',views.order,name="order"),

]