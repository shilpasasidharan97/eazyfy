from . import views
from django.urls import path


app_name = "pickupboy"

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("total_order/", views.total_order, name="total_order"),
    path("request-details/<str:id>/", views.product_details, name="request_details"),
    path("complete/<str:id>/", views.complete, name="complete"),
    path("fail/<str:id>/", views.fail, name="fail"),
    path("requote_first/<str:id>/", views.requote_first, name="requote_first"),
    path("requote_next/<str:id>/", views.requote_next, name="requote_next"),
    path("checkout/<str:id>/", views.checkout, name="checkout"),
]
