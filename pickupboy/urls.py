from django.urls import path
from . import views

app_name = 'pickupboy'

urlpatterns = [
    path('',views.index,name="index"),
    path('total-order',views.total_order,name="total-order"),
    path('product-validation',views.product_validation,name="product-validation"),
    path('product-details',views.product_details,name="product-details"),

    ]



    