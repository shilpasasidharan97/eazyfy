from . import views
from django.urls import path


app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("privacy-policy/", views.privacy_policy, name="privacy"),
    path("terms_of_use/", views.terms_of_use, name="terms_of_use"),
    path("sell_phone/", views.sell_phone, name="sell_phone"),
    path("sell_watches/", views.sell_watches, name="sell_watches"),
    path("buy_phone/", views.buy_phone, name="buy_phone"),
    path("repair_phone/", views.repair_phone, name="repair_phone"),
    path("comingsoon/", views.comingsoon, name="comingsoon"),
    path("find_new_gadget/", views.find_new_gadget, name="find_new_gadget"),
]
