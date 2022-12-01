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
    path('editfranchise/<int:id>',views.EditFranchise, name='editfranchise'),
    path('getprofiledata/<int:id>',views.getprofiledata,name='getprofiledata'),
    path('editform/<int:id>',views.editform,name='editform'),

    path('brand',views.brand,name='brand'),
    path('editbrand/<int:id>',views.editBrand, name='editbrand'),
    path('getbranddata/<int:id>',views.getbranddata, name='getbranddata'),
    path('deletebrand/<int:id>',views.DeleteBrand, name='deletebrand'),


    # path('editSpec/<int:id>',views.editSpec, name='editSpec'),
    # path('Deletespec/<int:id>',views.Deletespec, name='Deletespec'),

    path('model/<int:id>',views.Model,name='model'),
    path('getmodeldata/<int:id>',views.getModelData, name='getmodeldata'),
    path('editmodel/<int:id>',views.editModel, name='editmodel'),
    
    path('modelspecification/<int:id>',views.modelSpecification,name='modelspecification'),
    # path('getModelspec/<int:id>',views.getModelspec, name='getModelspec'),

    path('questions',views.questions,name='questions'),
    path('questionsadding',views.questionAdding,name='questionsadding'),
    # path('savedata/', views.savedata, name="savedata"),

    #trial
    path('questionsave', views.questsave, name="questionsave"),
    path('suquestionAdding', views.subquestionFirst, name="suquestionAdding"),
    path('suquestionAddingPage/<str:id>', views.subquestionPage, name="suquestionAddingPage"),
    # path('suquestionAddingdata', views.suquestionAddingData, name="suquestionAddingdata"),

    path('deductionsettings', views.deductionSettings, name="deductionsettings"),
    path('questionfordeduction', views.questionForDeduction, name="questionfordeduction"),


    path('userrequestlist',views.userRequestList,name='userrequestlist'),
    path('userdetails',views.userDetails,name='userdetails'),

    path('wallet',views.wallet,name='wallet'),
    path('viewpayment/<int:id>',views.viewPayment, name='viewpayment'),
    path('savepayment/<int:id>',views.savePayment,name='savepayment'),
    path('franchisewallet',views.franchiseWallet, name='franchisewallet'),
    path('transactionhistory',views.transactionHistory,name='transactionhistory'),

    path('test',views.test,name='test'),


    path('profile',views.profile,name='profile'),
    path('logout_view',views.logout_view,name='logout_view'),
     
]