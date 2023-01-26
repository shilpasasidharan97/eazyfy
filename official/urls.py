from . import views
from django.urls import path


app_name = "official"

urlpatterns = [
    path("", views.home, name="home"),
    path("userrequestlist/", views.user_request_list, name="userrequestlist"),
    path("request_details/<str:id>/", views.request_details, name="request_details"),
    path("loginpage/", views.loginPage, name="loginpage"),
    path("forgotpassword/", views.forgotPassword, name="forgotpassword"),
    path("franchise/", views.franchise, name="franchise"),
    path("franchisedetails/<int:id>/", views.viewFranchiseDetails, name="franchisedetails"),
    path("pickupboylist/<int:id>/", views.pickUpBoyList, name="pickupboylist"),
    path("deletefranchise/<int:id>/", views.delete_franchise, name="deletefranchise"),
    path("editfranchise/<int:id>/", views.EditFranchise, name="editfranchise"),
    path("getprofiledata/<int:id>/", views.getprofiledata, name="getprofiledata"),
    path("editform/<int:id>/", views.editform, name="editform"),
    path("wallet/", views.wallet, name="wallet"),
    path("viewpayment/<int:id>/", views.viewPayment, name="viewpayment"),
    path("savepayment/<int:id>/", views.save_payment, name="savepayment"),
    path("franchisewallet/", views.franchise_wallet, name="franchisewallet"),
    path("transactionhistory/", views.transactionHistory, name="transactionhistory"),
    path("profile/", views.profile, name="profile"),
    path("logout_view/", views.logout_view, name="logout_view"),
    path("settings/", views.official_settings, name="settings"),
    path("offers/", views.offers, name="offers"),
    path("delete_banner/<int:id>/", views.delete_banner, name="delete_banner"),
    path("delete_offer/<int:id>/", views.delete_offer, name="delete_offer"),
]
