from . import views
from django.urls import path


app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("privacy-policy/", views.privacy_policy, name="privacy"),
    path("terms_and_conditions/", views.terms_and_conditions, name="terms_and_conditions"),
    path("sell_phone/", views.sell_phone, name="sell_phone"),
    path("buy_phone/", views.buy_phone, name="buyphone"),
    path("repair_phone/", views.repair_phone, name="repair_phone"),
    path("payment/", views.payment, name="payment"),
    path("comingsoon/", views.comingsoon, name="comingsoon"),
    path("find_new_gadget/", views.find_new_gadget, name="find_new_gadget"),
    path("account/", views.account, name="account"),
]
