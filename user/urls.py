from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('terms',views.terms,name='terms'),
    path('login',views.login,name='login'),
    path('sell',views.sell,name='sell'),
    path('account',views.account,name='account'),
    path('privacy',views.privacy,name='privacy'),
    path('shops',views.shops,name='shops'),
    path('question',views.question,name='question'),


    path('my',views.my,name='my')
    
]