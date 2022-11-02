from django.urls import path
from . import views

app_name = 'official'

urlpatterns = [
    path('loginpage',views.loginPage,name='loginpage'),
    path('forgotpassword',views.forgotPassword,name='forgotpassword'),
    
    path('',views.home,name='home'),

    path('franchise',views.franchise,name='franchise'),
    path('franchisedetails/<int:id>',views.viewFranchiseDetails,name='franchisedetails'),
    path('pickupboylist/<int:id>',views.pickUpBoyList,name='pickupboylist'),
    path('deletefranchise/<int:id>',views.DeleteFranchise, name='deletefranchise'),

    path('brand',views.brand,name='brand'),
    path('model/<int:id>',views.Model,name='model'),
    path('modelspecification/<int:id>',views.modelSpecification,name='modelspecification'),

    path('questions',views.questions,name='questions'),
    path('questionsadding',views.questionAdding,name='questionsadding'),

    path('userrequestlist',views.userRequestList,name='userrequestlist'),
    path('userdetails',views.userDetails,name='userdetails'),

    path('wallet',views.wallet,name='wallet'),
    path('transactionhistory',views.transactionHistory,name='transactionhistory'),


    path('profile',views.profile,name='profile'),
    path('logout_view',views.logout_view,name='logout_view'),
     
]