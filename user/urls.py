from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('base',views.base,name='base'),
    path('',views.index,name='index'),
]