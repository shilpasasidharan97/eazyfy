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


    path('test',views.test,name="test"),

    

    path('sell',views.sell,name='sell'),
    path('shops',views.shops,name='shops'),
    path('question',views.question,name='question'),
    path('spec',views.spec,name='spec'),

    path('buy_phone',views.buyPhone,name='buyphone'),

    path('repair_phone',views.repairPhone,name='repair_phone'),
    path('payment',views.payment,name='payment'),
    path('comingsoon',views.comingsoon,name='comingsoon'),


    path('my',views.my,name='my')
    
]