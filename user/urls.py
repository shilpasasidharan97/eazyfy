from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('account',views.account,name='account'),
    path('privacy-policy',views.privacyAndPolicy,name='privacy'),
    path('terms-and-conditions',views.termsAndConditions,name='terms-and-conditions'),

    path('registration',views.UserRegistration,name='registration'),
    path('checkphonenumber',views.checkPhoneNumber,name='checkphonenumber'),
    path('otp-page/<str:id>',views.otp_fun,name="otp"),
 
    path('forgot',views.forgot,name="forgot"),
    path('resetPassword/<token>',views.resetPassword,name="resetPassword"),
    path('resendotp/<token>',views.resendOtp,name="resendotp"),
    path('login',views.customerlogin,name="login"),


    path('sell-phone',views.sellPhone,name='sell-phone'),
    path('sell',views.sell,name='sell'),
    path('shops/<str:id>',views.shops,name='shops'),
    path('question/<str:id>',views.question,name='question'),


    path('spec/<str:id>',views.spec,name='spec'),
    path('getspecdata/<int:id>',views.getspecdata,name='getspecdata'),

    path('buy_phone',views.buyPhone,name='buyphone'),
    path('order-confirm',views.orderConfirm,name='order-confirm'),

    path('repair_phone',views.repairPhone,name='repair_phone'),

    path('imagetype',views.imagetype,name='imagetype'),

    path('payment',views.payment,name='payment'),
    path('comingsoon',views.comingsoon,name='comingsoon'),
    path('findnewgadget',views.findnewgadget,name='findnewgadget'),
    path('user-logout',views.userLogout,name='user-logout'),
    path('objective_type',views.objective_type,name='objective_type'),
    path('image_type',views.image_type,name='image_type'),

    # path('test',views.test,name='test'),
     
]