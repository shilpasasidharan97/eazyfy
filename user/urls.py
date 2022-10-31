from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('terms-and-conditions',views.termsAndConditions,name='terms-and-conditions'),
    path('login',views.login,name='login'),
    path('sell',views.sell,name='sell'),
    path('account',views.account,name='account'),
    path('privacy',views.privacy,name='privacy'),
    path('shops',views.shops,name='shops'),
    path('question',views.question,name='question'),
    path('spec',views.spec,name='spec'),
    path('buy',views.buy,name='buy'),
    path('repair',views.repair,name='repair'),
    path('payment',views.payment,name='payment'),
    path('comingsoon',views.comingsoon,name='comingsoon'),


    path('my',views.my,name='my')
    
]