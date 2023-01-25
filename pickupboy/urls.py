from . import views
from django.urls import path


app_name = "pickupboy"

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("total-order/", views.total_order, name="total-order"),
    path("customer-selfy/", views.customer_selfy, name="customer-selfy"),
    path("product-details/", views.product_details, name="product-details"),
    path("verification-questions/", views.verification_questions, name="verification-questions"),
    path("complete-selfy/", views.complete_selfy, name="complete-selfy"),
    path("complete/", views.complete, name="complete"),
    path("fail/", views.fail, name="fail"),
    path("requote/", views.requote, name="requote"),
    path("requote-selfy/", views.requote_selfy, name="requote-selfy"),
    path("checkout/", views.checkout, name="checkout"),
]
