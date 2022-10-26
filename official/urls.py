from django.urls import path
from . import views

app_name = 'official'

urlpatterns = [
    path('loginpage',views.loginPage,name='loginpage'),
    path('forgotpassword',views.forgotPassword,name='forgotpassword'),
    
    path('',views.home,name='home'),

    path('franchise',views.franchise,name='franchise'),
    path('franchisedetails',views.viewFranchiseDetails,name='franchisedetails'),
    path('pickupboylist',views.pickUpBoyList,name='pickupboylist'),

    path('brand',views.brand,name='brand'),
    path('model',views.Model,name='model'),
    path('modelspecification',views.modelSpecification,name='modelspecification'),
    path('questionsadding',views.questionAdding,name='questionsadding'),

    path('userrequestlist',views.userRequestList,name='userrequestlist'),
    path('userdetails',views.userDetails,name='userdetails'),

    path('wallet',views.wallet,name='wallet'),
    path('transactionhistory',views.transactionHistory,name='transactionhistory'),

    path('profile',views.profile,name='profile'),
     
]