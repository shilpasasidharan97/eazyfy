from . import views
from django.urls import path


app_name = "user"

urlpatterns = [
    path("sell/<str:slug>/", views.pick_model, name="pick_model"),
    path("registration/", views.user_registration, name="registration"),
    path("checkphonenumber/", views.check_phone_number, name="checkphonenumber"),
    path("otp-page/<str:id>/", views.otp_fun, name="otp"),
    path("forgot/", views.forgot, name="forgot"),
    path("reset_password/<token>/", views.reset_password, name="reset_password"),
    path("login/", views.customer_login, name="login"),
    path("resendotp/<token>/", views.resend_otp, name="resendotp"),
    path("varant/survey/<str:id>/", views.question, name="question"),
    # ajax
    path("saveanswer/", views.save_answer, name="save_answer"),
    path("sell/model/<str:slug>/", views.device_page, name="device_page"),
    path("getspecdata/<int:id>/", views.getspecdata, name="getspecdata"),
    path("user-logout/", views.user_logout, name="user-logout"),
]
