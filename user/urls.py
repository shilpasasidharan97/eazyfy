from . import views
from django.urls import path


app_name = "user"

urlpatterns = [
    path("sell/model/variant/survey/<str:id>/", views.question, name="question"),
    path("sell/info/<str:id>/", views.info_page, name="info_page"),
    path("sell/request/<str:id>/", views.request_page, name="request_page"),
    path("accounts/login/", views.login_page, name="auth_login"),
    path("accounts/logout/", views.logout_page, name="auth_logout"),
    path("accounts/register/", views.register_page, name="registration_register"),
    path("accounts/verify/<int:phone/", views.verify_page, name="verify_page"),
    path("accounts/verify/resend/<int:phone/", views.resend_page, name="resend_page"),
    # later
    # path("registration/", views.user_registration, name="registration"),
    # path("checkphonenumber/", views.check_phone_number, name="checkphonenumber"),
    # path("otp-page/<str:id>/", views.otp_fun, name="otp"),
    # path("forgot/", views.forgot, name="forgot"),
    # path("reset_password/<token>/", views.reset_password, name="reset_password"),
    # path("login/", views.customer_login, name="login"),
    # path("resendotp/<token>/", views.resend_otp, name="resendotp"),
    # path("user_logout/", views.user_logout, name="user_logout"),
]
