from . import views
from django.urls import path


app_name = "franchise"

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("add-pickupboy/", views.add_pickupboy, name="add-pickupboy"),
    path("order/", views.order, name="order"),
    path("order-details/<int:id>/", views.order_details, name="order_details"),
    path("deletepickupboy/<int:id>/", views.Deletepickupboy, name="deletepickupboy"),
    path("editform/<int:id>/", views.editform, name="editform"),
    path("getprofiledata/<int:id>/", views.getprofiledata, name="getprofiledata"),
    path("transactions/", views.transactions, name="transactions"),
    path("order/accept/<int:id>/", views.accept_order, name="accept_order"),
]
